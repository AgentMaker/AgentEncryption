# Author: Acer Zhang
# Datetime: 2021/10/27
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import os
import json
import base64
import pickle

from agentenc.ops import EncryptOp


class Encryptor:
    def __init__(self, encrypt_op: EncryptOp):
        """
        加密器基类

        :param 
            encrypt_op(EncryptOp): 加密相关OP
        """
        self.encrypt_op = encrypt_op

    @staticmethod
    def bytes2str(input: bytes) -> str:
        """
        bytes to base64 str (inp -> data:data/agt;base64,{base64[inp]})

        :param 
            inp(bytes): 输入

        :return
            output(str): 输出 
        """
        output = base64.b64encode(input).decode('UTF-8')
        return f'data:data/agt;base64,{output}'

    @staticmethod
    def str2bytes(input: str) -> bytes:
        """
        base64 str to bytes (data:data/agt;base64,{base64[inp]} -> inp)

        :param 
            inp(bytes): 输入

        :return
            output(str): 输出
        """
        if isinstance(input, str) and input[:21] == 'data:data/agt;base64,':
            input = base64.b64decode(input[21:].encode('UTF-8'))
            assert type(input) == bytes
        return input

    @staticmethod
    def check_and_convert(input: any) -> any:
        """
        检查并递归转换 bytes -> bytes_str

        :param 
            inp(any): 输入

        :return
            output(any): 输出
        """
        if isinstance(input, dict):
            _input = input.copy()
            for k in input.keys():
                _input[k] = Encryptor.check_and_convert(input[k])
            return _input
        elif isinstance(input, (list, tuple)):
            _input = input.copy()
            for i in range(len(input)):
                _input[i] = Encryptor.check_and_convert(input[i])
            return _input
        elif isinstance(input, bytes):
            return Encryptor.bytes2str(input)
        elif isinstance(input, (str, int, float, bool, None)):
            return input
        else:
            raise ValueError('Please check inp data type.')

    @staticmethod
    def resume_and_convert(input: any) -> any:
        """
        恢复并递归转换 bytes_str -> bytes

        :param 
            inp(any): 输入

        :return
            output(any): 输出
        """
        if isinstance(input, dict):
            for k in input.keys():
                input[k] = Encryptor.resume_and_convert(input[k])
            return input
        elif isinstance(input, (list, tuple)):
            for i in range(len(input)):
                input[i] = Encryptor.resume_and_convert(input[i])
            return input
        elif isinstance(input, str):
            return Encryptor.str2bytes(input)
        elif isinstance(input, (int, float, bool, None)):
            return input
        else:
            raise ValueError('Please check inp data type.')

    def encode(self, inp: any, output: str, format: str = 'pkl', keys_saving_path: str = None) -> dict:
        """
        加密函数

        :param 
            inp(any): 输入的需要加密的数据
            output(str): 输出的文件名称
            format(str: pkl [pkl / json / pdmodel]): 输出的数据格式

        :return
            private_params(dict): 加密器的私密参数，如密钥等

        :format details
            pkl: 此格式支持的加密数据类型较多，并且附带 python 解密函数，可依靠自身进行解密，但只可以在 python 端进行解密操作
            json: 此格式支持如下几种数据类型 (dict, list, tuple, str, int, float, bool, bytes->bytes_str, None), 可以在任意语言中读取和解密，需搭配对应语言的解密函数进行解密操作
        """
        if format == 'pkl':
            encrypt_data = self.encrypt_op.encode(
                pickle.dumps(inp, protocol=4))

            with open(output + '.pkl', "wb") as file:
                pickle.dump({
                    'datas': Encryptor.bytes2str(encrypt_data),
                    'params': self.encrypt_op.get_public_params(),
                    'decode': self.encrypt_op.decode
                }, file, protocol=4)

        elif format == 'json':
            encrypt_data = self.encrypt_op.encode(
                json.dumps(Encryptor.check_and_convert(inp)).encode('UTF-8'))

            with open(output + '.json', "w") as file:
                json.dump({
                    'datas': Encryptor.bytes2str(encrypt_data),
                    'params': Encryptor.check_and_convert(self.encrypt_op.get_public_params())
                }, file)
        elif format == "pdmodel":
            pdiparams = inp + ".pdiparams"
            pdmodel = inp + ".pdmodel"
            assert os.path.exists(pdiparams), FileExistsError(pdiparams + "文件不存在，请检查输入路径是否正确")
            assert os.path.exists(pdmodel), FileExistsError(pdmodel + "文件不存在，请检查输入路径是否正确")
            with open(pdiparams, "rb") as f:
                pdiparams = f.read()
            with open(pdmodel, "rb") as f:
                pdmodel = f.read()

            encrypt_data = pdiparams + b"AgentEncryptionFlags" + pdmodel

            encrypt_data = self.encrypt_op.encode(encrypt_data)
            with open(output + '.EncPdModel', "wb") as file:
                pickle.dump({
                    'data': Encryptor.bytes2str(encrypt_data),
                    'params': self.encrypt_op.get_public_params(),
                    'decode': self.encrypt_op.decode
                }, file, protocol=4)

        else:
            raise ValueError('Please check the format type.')

        return self.encrypt_op.get_private_params(keys_saving_path)

    @staticmethod
    def decode(inp: str, decode=None, **kwargs) -> any:
        """
        解密函数

        :param 
            inp(str): 输入的文件路径
            decode(func): 解密函数 
            **kwargs: 解密所需的一些其他参数

        :return
            pure_datas(any): 原始数据
        """
        ext = os.path.splitext(inp)[1]

        # 加载机密数据包
        if ext == '.pkl' or ext == ".EncPdModel":
            with open(inp, "rb") as file:
                encrypt_package = pickle.load(file)
        elif ext == '.json':
            with open(inp, "r") as file:
                encrypt_package = json.load(file)
        else:
            raise ValueError('Please check inp path.')

        # 解码公开参数
        params = encrypt_package['params']
        params = Encryptor.resume_and_convert(params)

        # 解码加密数据
        encrypt_data = Encryptor.str2bytes(encrypt_package['data'])
        decode = encrypt_package.get('decode', decode)
        pure_data = decode(encrypt_data, **kwargs, **params)

        # 重新加载原始数据
        if ext == '.pkl':
            output = pickle.loads(pure_data)
        elif ext == '.json':
            output = json.loads(pure_data.decode('UTF-8'))
            output = Encryptor.resume_and_convert(output)
        elif ext == ".EncPdModel":
            pdiparams, pdmodel = pure_data.split(b"AgentEncryptionFlags")
            from paddle.inference import Config
            output = Config()
            output.set_model_buffer(pdmodel, len(pdmodel), pdiparams, len(pdiparams))
            return output
        else:
            raise ValueError('Please check inp data type.')

        return output
