from agentenc.encryptors import Encryptor
from agentenc.ops import AESEncryptOp


class AESEncryptor(Encryptor):
    def __init__(self, bits: int = 128, mode: str = 'ECB'):
        '''
        AES 加密器

        :param 
            bits(int: 128): 加密使用的 bit 数
            mode(str: ECB): 加密类型，可选：['ECB', 'CBC', 'CFB', 'OFB', 'CTR', 'OPENPGP', 'CCM', 'EAX', 'SIV', 'GCM', 'OCB']
        '''
        super(AESEncryptor, self).__init__(AESEncryptOp(bits, mode))

    @staticmethod
    def decode(input: str, password: bytes, iv: bytes) -> any:
        '''
        解密函数

        :param 
            input(str): 输入的文件路径
            password(bytes): AES 密钥
            iv(bytes): 偏移值

        :return
            pure_datas(any): 原始数据
        '''
        return Encryptor.decode(
            input=input,
            password=password,
            iv=iv,
            decode=AESEncryptOp.decode
        )
