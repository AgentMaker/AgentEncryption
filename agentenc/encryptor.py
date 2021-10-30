# Author: Acer Zhang
# Datetime: 2021/10/27
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import os
import json
import base64
import pickle

from Crypto.Cipher import AES
from agentenc.ops import EncryptOp, RSAEncryptOp, AESEncryptOp


class Encryptor:
    def __init__(self,
                 encrypt_op: EncryptOp):
        """
        加密器基类

        :param 
            encrypt_op(EncryptOp): 加密相关OP
        """
        self.encrypt_op = encrypt_op

    def encode(self, input: any, output: str, format: str = 'pkl', keys_saving_path: str = None) -> dict:
        '''
        加密函数

        :param 
            input(any): 输入的需要加密的数据
            output(str): 输出的文件名称
            format(str: pkl [pkl / json{输入数据目前仅支持单层字典}]): 输出的数据格式

        :return
            private_params(dict): 加密器的私密参数，如密钥等

        :format details
            pkl: 此格式支持的加密数据类型较多，并且附带 python 解密函数，可依靠自身进行解密，但只可以在 python 端进行解密操作
            json: 此格式支持如下几种数据类型 (dict, list, tuple, str, int, float, bool, bytes->base64[UTF-8 str]) 组成的单层 dict 可以在任意语言中读取和解密，需搭配对应语言的解密函数进行解密操作
        '''
        if format == 'pkl':
            encrypt_datas = self.encrypt_op.encode(pickle.dumps(input))

            with open(output+'.pkl', "wb") as file:
                pickle.dump({
                    'datas': str(base64.b64encode(encrypt_datas).decode('UTF-8')),
                    'params': self.encrypt_op.get_public_params(),
                    'decode': self.encrypt_op.decode
                }, file)
        elif format == 'json':
            encode_input = input.copy()

            # convert bytes to str
            for k in encode_input.keys():
                if isinstance(encode_input[k], bytes):
                    encode_input[k] = '##base64##' + \
                        str(base64.b64encode(encode_input[k]).decode('UTF-8'))
                elif not isinstance(encode_input[k], (dict, list, tuple, str, int, float, bool)):
                    raise ValueError('Please check input data type.')

            encrypt_datas = self.encrypt_op.encode(
                json.dumps(encode_input).encode('UTF-8'))

            with open(output+'.json', "w") as file:
                json.dump({
                    'datas': str(base64.b64encode(encrypt_datas).decode('UTF-8')),
                    'params': self.encrypt_op.get_params()
                }, file)
        return self.encrypt_op.get_private_params(keys_saving_path)

    @staticmethod
    def decode(input: str, decode=None, **kwargs) -> any:
        '''
        解密函数

        :param 
            input(str): 输入的文件路径
            decode(func): 解密函数 
            **kwargs: 解密所需的一些其他参数

        :return
            pure_datas(any): 原始数据
        '''
        ext = os.path.splitext(input)[1]
        if ext == '.pkl':
            with open(input, "rb") as file:
                encrypt_package = pickle.load(file)
        elif ext == '.json':
            with open(input, "r") as file:
                encrypt_package = json.load(file)
        else:
            raise ValueError('Please check input path.')

        params = encrypt_package['params']
        encrypt_datas = base64.b64decode(
            encrypt_package['datas'].encode('UTF-8'))
        decode = encrypt_package.get('decode', decode)
        pure_datas = decode(encrypt_datas, **kwargs, **params)

        if ext == '.pkl':
            output = pickle.loads(pure_datas)
        elif ext == '.json':
            output = json.loads(pure_datas.decode('UTF-8'))
            for k in output.keys():
                if isinstance(output[k], str) and output[k][:10] == '##base64##':
                    output[k] = base64.b64decode(
                        output[k][10:].encode('UTF-8'))
        return output


class RSAEncryptor(Encryptor):
    def __init__(self, bits: int = 1024):
        '''
        RSA 加密器

        :param 
            bits(int: 1024): 加密使用的 bit 数
        '''
        super(RSAEncryptor, self).__init__(RSAEncryptOp(bits))

    @staticmethod
    def decode(input: str, private_pem: bytes) -> any:
        '''
        解密函数

        :param 
            input(str): 输入的文件路径
            private_pem(bytes): RSA 私钥用于数据解密

        :return
            pure_datas(any): 原始数据
        '''
        return Encryptor.decode(
            input=input,
            private_pem=private_pem,
            decode=RSAEncryptOp.decode
        )


class AESEncryptor(Encryptor):
    def __init__(self, bits: int = 128, mode: int = AES.MODE_OFB):
        '''
        AES 加密器

        :param 
            bits(int: 128): 加密使用的 bit 数
            mode(int: AES.MODE_OFB): AES 加密类型
        '''
        super(AESEncryptor, self).__init__(AESEncryptOp(bits, mode))

    @staticmethod
    def decode(input: str, password: bytes) -> any:
        '''
        解密函数

        :param 
            input(str): 输入的文件路径
            password(bytes): AES 密钥

        :return
            pure_datas(any): 原始数据
        '''
        return Encryptor.decode(
            input=input,
            password=password,
            decode=AESEncryptOp.decode
        )
