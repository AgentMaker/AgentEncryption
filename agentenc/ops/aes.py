# Author: Acer Zhang
# Datetime: 2021/10/27
# Copyright belongs to the author.
# Please indicate the source for reprinting.
from os import urandom
from Crypto.Cipher import AES

from agentenc.ops import EncryptOp


class AESEncryptOp(EncryptOp):
    def __init__(self, bits: int = 128, mode: int = AES.MODE_ECB):
        """
        AES 加密算子

        :param 
            bits(int: 128): 加密 bit 数
            mode(int: 1[AES.MODE_ECB]): 加密类型
        """
        super().__init__()
        self.length = bits // 8
        self.mode = mode
        self.password = urandom(self.length)
        self.iv = urandom(16)
        self.aes = AES.new(key=self.password, mode=self.mode, iv=self.iv)

    def get_private_params(self, save_path: str = None) -> dict:
        """
        获取并保存密钥

        :param 
            save_path(str: None): 密钥保存目录

        :return
            private_params(dict): {'password': AES 密钥}

        :save file details
            "{save_path}.PUBLIC": AES 公钥
            "{save_path}.PRIVATE": AES 私钥
        """
        if save_path:
            with open(f'{save_path}.PASSWORD', "wb") as f:
                f.write(self.password)
        return {'password': self.password}

    def get_public_params(self) -> dict:
        """
        获取解密所需的公开参数

        :return
            public_params(dict): {'mode': 加密类型, 'iv': 偏移值}
        """
        return {
            'mode': self.mode,
            'iv': self.iv
        }

    def encode(self, input: bytes) -> bytes:
        """
        AES 加密

        :param 
            input(bytes): 输入数据

        :return
            output(bytes): 加密数据
        """
        count = len(input)
        if count % self.length != 0:
            add = self.length - (count % self.length)
        else:
            add = 0

        input = input + (b'\x00' * add)
        output = self.aes.encrypt(input)
        return output

    @staticmethod
    def decode(input: bytes, mode: int, iv: bytes, password: bytes) -> bytes:
        """
        AES 解密

        :param 
            input(bytes): 加密数据
            mode(int: 1[AES.MODE_ECB]): 加密类型
            iv(bytes): 偏移值
            password(bytes): AES 密钥

        :return
            output(bytes): 原始数据
        """
        aes = AES.new(key=password, mode=mode, iv=iv)
        output = aes.decrypt(input)
        output = output.rstrip(b'\x00')
        return output
