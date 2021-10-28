# Author: Acer Zhang
# Datetime: 2021/10/27
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import os

from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

from agentenc.ops import BaseEncryptOp


PRIVATE_FILE = "PRIVATE"
PUBLIC_FILE = "PUBLIC"


class RSAEncryptOp(BaseEncryptOp):
    def __init__(self, bits: int = 1024):
        """
        这里主要定义的是成员变量
        :param bits:
        """
        super().__init__()
        self.bits = bits
        self.rsa = RSA.generate(self.bits, Random.new().read)
        self.private_pem = self.rsa.exportKey()
        self.public_pem = self.rsa.publickey().exportKey()

        self.length = bits // 8 - 11

    def prepare(self, *arg):
        """
        prepare将传入Maker的self对象，所有与Maker相关变量可再此处进行处理
        """
        save_path = arg[0].save_path
        with open(os.path.join(save_path, PRIVATE_FILE), "wb") as f:
            f.write(self.private_pem)
        with open(os.path.join(save_path, PUBLIC_FILE), "wb") as f:
            f.write(self.public_pem)

    def encode(self, text, *args, **kwargs) -> bytes:
        """
        该部分为encoder的部分，传入bytes返回加密的bytes
        """
        rsa_key = RSA.importKey(self.public_pem)
        cipher = PKCS1_v1_5.new(rsa_key)
        cipher_text_ = []

        for i in range(0, len(text), self.length):
            cipher_text_.append(cipher.encrypt(text[i:i + self.length]))
        cipher_text = b""
        for item in cipher_text_:
            cipher_text += item
        return cipher_text

    def get_params(self) -> dict:
        """
        返回一个字典，该字典中不包含任何不想让客户端知晓的变量，但需要包含客户端解密所需要的参数
        """
        return {"length": self.length + 11}

    @staticmethod
    def decode(text, *arg, **kwargs) -> bytes:
        """
        同encoder，该部分将传入待解密的文本，其中arg为Maker的self对象
        """
        private_pem = kwargs['private_pem']
        rsa_key = RSA.importKey(private_pem)
        length = kwargs["length"]

        cipher = PKCS1_v1_5.new(rsa_key)
        plain_text_ = []
        for i in range(0, len(text), length):
            plain_text_.append(cipher.decrypt(text[i:i + length], "解密失败"))
        text = b""
        for item in plain_text_:
            text += item
        return text
