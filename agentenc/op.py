# Author: Acer Zhang
# Datetime: 2021/10/27 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import os
import base64

from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

from agentenc.base import BaseEncryptOp

PRIVATE_FILE = "PRIVATE"
PUBLIC_FILE = "PUBLIC"


class RSAOp(BaseEncryptOp):
    def __init__(self, bits: int = 1024):
        super().__init__()
        self.bits = bits
        self.rsa = RSA.generate(self.bits, Random.new().read)
        self.private_pem = self.rsa.exportKey()
        self.public_pem = self.rsa.publickey().exportKey()

        self.length = bits // 8 - 11

    def prepare(self, save_path):
        with open(os.path.join(save_path, PRIVATE_FILE), "wb") as f:
            f.write(self.private_pem)
        with open(os.path.join(save_path, PUBLIC_FILE), "wb") as f:
            f.write(self.public_pem)

    def encoder(self, text, *args, **kwargs) -> bytes:
        rsa_key = RSA.importKey(self.public_pem)
        cipher = PKCS1_v1_5.new(rsa_key)
        cipher_text_ = []

        for i in range(0, len(text), self.length):
            cipher_text_.append(cipher.encrypt(text[i:i + self.length]))
        cipher_text = b""
        for item in cipher_text_:
            cipher_text += item
        return cipher_text

    def get_param(self) -> dict:
        return {"length": self.length + 11}

    @staticmethod
    def decoder(text, *arg, **kwargs) -> bytes:
        self = arg[0]
        load_path = self.load_path
        with open(os.path.join(load_path, PRIVATE_FILE), "rb") as f:
            rsa_key = RSA.importKey(f.read())
        length = kwargs["length"]

        cipher = PKCS1_v1_5.new(rsa_key)
        plain_text_ = []
        for i in range(0, len(text), length):
            plain_text_.append(cipher.decrypt(text[i:i + length], "解密失败"))
        text = b""
        for item in plain_text_:
            text += item
        return text
