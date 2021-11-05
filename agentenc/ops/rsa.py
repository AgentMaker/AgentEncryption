# Author: Acer Zhang
# Datetime: 2021/10/27
# Copyright belongs to the author.
# Please indicate the source for reprinting.

from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

from agentenc.ops import EncryptOp


PRIVATE_FILE = "PRIVATE"
PUBLIC_FILE = "PUBLIC"


class RSAEncryptOp(EncryptOp):
    def __init__(self, bits: int = 1024, public_key: bytes = None):
        """
        RSA 加密算子

        :param 
            bits(int: 1024): 加密 bit 数
            public_key(bytes: None): RSA 公钥，格式为 b'-----BEGIN PUBLIC KEY-----...-----END PUBLIC KEY----- 的 bytes，默认随机生成
        """
        super().__init__()
        self.bits = bits

        if public_key is not None:
            self.private_key = None
            self.public_key = public_key
        else:
            self.rsa = RSA.generate(self.bits, Random.new().read)
            self.private_key = self.rsa.exportKey()
            self.public_key = self.rsa.publickey().exportKey()

        self.length = bits // 8 - 11

    def get_private_params(self, save_path: str = None) -> dict:
        """
        获取并保存密钥

        :param 
            save_path(str: None): 密钥保存目录

        :return
            private_params(dict): {'private_key': RSA 私钥, 'public_key': RSA 公钥}

        :save file details
            "{save_path}.PUBLIC": RSA 公钥
            "{save_path}.PRIVATE": RSA 私钥
        """
        if save_path:
            with open(f'{save_path}.{PUBLIC_FILE}', "wb") as f:
                f.write(self.public_key)

            if self.private_key is not None:
                with open(f'{save_path}.{PRIVATE_FILE}', "wb") as f:
                    f.write(self.private_key)

        if self.private_key is not None:
            return {
                'public_key': self.public_key,
                'private_key': self.private_key
            }
        else:
            return {
                'public_key': self.public_key
            }

    def get_public_params(self) -> dict:
        """
        获取解密所需的公开参数

        :return
            public_params(dict): {'length': 加密长度}
        """
        return {"length": self.length + 11}

    def encode(self, input: bytes) -> bytes:
        """
        RSA 加密

        :param 
            inp(bytes): 输入数据

        :return
            output(bytes): 加密数据
        """
        rsa_key = RSA.importKey(self.public_key)
        cipher = PKCS1_v1_5.new(rsa_key)
        cipher_text_ = []

        for i in range(0, len(input), self.length):
            cipher_text_.append(cipher.encrypt(input[i:i + self.length]))
        output = b""
        for item in cipher_text_:
            output += item
        return output

    @staticmethod
    def decode(input: bytes, length: int, private_key: bytes) -> bytes:
        """
        RSA 解密

        :param 
            inp(bytes): 加密数据
            length(int): 加密长度
            private_key(bytes): 私钥

        :return
            output(bytes): 原始数据
        """
        rsa_key = RSA.importKey(private_key)
        cipher = PKCS1_v1_5.new(rsa_key)
        plain_text_ = []
        for i in range(0, len(input), length):
            plain_text_.append(cipher.decrypt(
                input[i:i + length], "Decode error."))
        output = b""
        for item in plain_text_:
            output += item
        return output
