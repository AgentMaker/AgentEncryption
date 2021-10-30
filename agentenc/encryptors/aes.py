from agentenc.encryptors import Encryptor
from agentenc.ops import AESEncryptOp


class AESEncryptor(Encryptor):
    def __init__(self, bits: int = 128, mode: str = 'ECB', iv: bytes = None, key: bytes = None):
        '''
        AES 加密器

        :param 
            bits(int: 128): 加密使用的 bit 数
            mode(str: ECB): 加密类型，可选：['ECB', 'CBC', 'CFB', 'OFB', 'CTR', 'OPENPGP', 'CCM', 'EAX', 'SIV', 'GCM', 'OCB']
            iv(bytes: None): 偏移值，长度为 16 bytes ，默认随机生成
            key(bytes: None): AES 密钥，长度为 (bits // 8) bytes ，默认随机生成
        '''
        super(AESEncryptor, self).__init__(
            AESEncryptOp(
                bits=bits,
                mode=mode,
                iv=iv,
                key=key
            )
        )

    @staticmethod
    def decode(input: str, key: bytes, iv: bytes) -> any:
        '''
        解密函数

        :param 
            input(str): 输入的文件路径
            key(bytes): AES 密钥
            iv(bytes): 偏移值

        :return
            pure_datas(any): 原始数据
        '''
        return Encryptor.decode(
            input=input,
            key=key,
            iv=iv,
            decode=AESEncryptOp.decode
        )
