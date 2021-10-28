# Author: Acer Zhang
# Datetime: 2021/10/27
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import pickle
from agentenc.ops import EncryptOp, RSAEncryptOp


class Encryptor:
    def __init__(self,
                 encrypt_op: EncryptOp):
        """
        资源文件加密基类
        :param encrypt_op: 加密相关OP
        """
        self.encrypt_op = encrypt_op

    def encode(self, input: dict, output: str):
        encrypt_datas = self.encrypt_op.encode(pickle.dumps(input))
        with open(output, "wb") as file:
            pickle.dump({
                'datas': encrypt_datas,
                'params': self.encrypt_op.get_params(),
                'decode': self.encrypt_op.decode
            }, file)

    @staticmethod
    def decode(input: str, **kwargs):
        with open(input, "rb") as file:
            encrypt_package = pickle.load(file)
        params = encrypt_package['params']
        encrypt_datas = encrypt_package['datas']
        decode = encrypt_package['decode']
        pure_datas = decode(encrypt_datas, **kwargs, **params)
        output = pickle.loads(pure_datas)
        return output


class RSAEncryptor(Encryptor):
    def __init__(self, bits: int = 1024):
        super(RSAEncryptor, self).__init__(RSAEncryptOp(bits))

    def decode(input: str, private_pem: bytes):
        return Encryptor.decode(input=input, private_pem=private_pem)
