# Author: Acer Zhang
# Datetime: 2021/10/27
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import os
import json
import base64
import pickle

from agentenc.ops import EncryptOp, RSAEncryptOp


class Encryptor:
    def __init__(self,
                 encrypt_op: EncryptOp):
        """
        加密器

        :param 
            encrypt_op(EncryptOp): 加密相关OP
        """
        self.encrypt_op = encrypt_op

    def encode(self, input: dict, output: str, with_decode: bool = True):
        '''
        加密函数

        :param 
            input(dict): 输入的需要加密的字典数据
            output(str): 输出的文件名称
            with_decode(bool: True): 是否附带解密函数

        :output format
            with_decode：.agt 格式的文件，附带 python 解密函数，可依靠自身进行解密，但只可以在 python 端进行解密操作
            without_decode: .json 格式文件，可以在任意语言中读取和解密，需搭配对应语言的解密函数进行解密操作
        '''
        encrypt_datas = self.encrypt_op.encode(pickle.dumps(input))
        if with_decode:
            with open(output+'.agt', "wb") as file:
                pickle.dump({
                    'datas': str(base64.b64encode(encrypt_datas).decode('UTF-8')),
                    'params': self.encrypt_op.get_params(),
                    'decode': self.encrypt_op.decode
                }, file)
        else:
            with open(output+'.json', "w") as file:
                json.dump({
                    'datas': str(base64.b64encode(encrypt_datas).decode('UTF-8')),
                    'params': self.encrypt_op.get_params()
                }, file)

    @staticmethod
    def decode(input: str, decode=None, **kwargs):
        '''
        解密函数

        :param 
            input(str): 输入的文件路径
            decode(func): 解密函数 
            **kwargs: 解密所需的一些其他参数
        '''
        ext = os.path.splitext(input)[1]
        if ext == '.agt':
            with open(input, "rb") as file:
                encrypt_package = pickle.load(file)
        elif ext == '.json':
            with open(input, "r") as file:
                encrypt_package = json.load(file)

        params = encrypt_package['params']
        encrypt_datas = base64.b64decode(
            encrypt_package['datas'].encode('UTF-8'))
        decode = encrypt_package.get('decode', decode)
        pure_datas = decode(encrypt_datas, **kwargs, **params)
        output = pickle.loads(pure_datas)
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
    def decode(input: str, private_pem: bytes):
        '''
        解密函数

        :param 
            input(str): 输入的文件路径
            private_pem(bytes): RSA 私钥用于数据解密
        '''
        return Encryptor.decode(
            input=input,
            private_pem=private_pem,
            decode=RSAEncryptOp.decode
        )
