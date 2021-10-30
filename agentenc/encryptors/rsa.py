from agentenc.encryptors import Encryptor
from agentenc.ops import RSAEncryptOp


class RSAEncryptor(Encryptor):
    def __init__(self, bits: int = 1024, public_key: bytes = None):
        '''
        RSA 加密器

        :param 
            bits(int: 1024): 加密使用的 bit 数
            public_key(bytes: None): RSA 公钥，格式为 b'-----BEGIN PUBLIC KEY-----...-----END PUBLIC KEY----- 的 bytes，默认随机生成
        '''
        super(RSAEncryptor, self).__init__(RSAEncryptOp(bits, public_key))

    @staticmethod
    def decode(input: str, private_key: bytes) -> any:
        '''
        解密函数

        :param 
            input(str): 输入的文件路径
            private_key(bytes): RSA 私钥用于数据解密

        :return
            pure_datas(any): 原始数据
        '''
        return Encryptor.decode(
            input=input,
            private_key=private_key,
            decode=RSAEncryptOp.decode
        )
