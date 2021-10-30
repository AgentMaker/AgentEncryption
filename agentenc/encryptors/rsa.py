from agentenc.encryptors import Encryptor
from agentenc.ops import RSAEncryptOp


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
