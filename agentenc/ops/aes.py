# Author: Acer Zhang
# Datetime: 2021/10/27
# Copyright belongs to the author.
# Please indicate the source for reprinting.

from os import urandom
from Crypto.Cipher import AES

from agentenc.ops import EncryptOp


IV_FILE = "IV"
PASSWORD_FILE = "PASSWORD"


# AES Mode Switch
ASE_MODES = {
    'ECB': AES.MODE_ECB,
    'CBC': AES.MODE_CBC,
    'CFB': AES.MODE_CFB,
    'OFB': AES.MODE_OFB,
    'CTR': AES.MODE_CTR,
    'OPENPGP': AES.MODE_OPENPGP,
    'CCM': AES.MODE_CCM,
    'EAX': AES.MODE_EAX,
    'SIV': AES.MODE_SIV,
    'GCM': AES.MODE_GCM,
    'OCB': AES.MODE_OCB
}


class AESEncryptOp(EncryptOp):
    def __init__(self, bits: int = 128, mode: str = 'ECB'):
        """
        AES 加密算子

        :param 
            bits(int: 128): 加密 bit 数
            mode(str: ECB): 加密类型，可选：['ECB', 'CBC', 'CFB', 'OFB', 'CTR', 'OPENPGP', 'CCM', 'EAX', 'SIV', 'GCM', 'OCB']
        """
        super().__init__()
        self.length = bits // 8
        self.mode = mode
        self.password = urandom(self.length)
        self.iv = urandom(16)
        self.aes = AES.new(
            key=self.password,
            mode=ASE_MODES[self.mode],
            iv=self.iv
        )

    def get_private_params(self, save_path: str = None) -> dict:
        """
        获取并保存密钥

        :param 
            save_path(str: None): 密钥保存目录

        :return
            private_params(dict): {'password': AES 密钥, 'iv': 偏移值}

        :save file details
            "{save_path}.PASSWORD": AES 密钥
            "{save_path}.IV": 偏移值
        """
        if save_path:
            with open(f'{save_path}.{PASSWORD_FILE}', "wb") as f:
                f.write(self.password)
            with open(f'{save_path}.{IV_FILE}', "wb") as f:
                f.write(self.iv)
        return {
            'password': self.password,
            'iv': self.iv
        }

    def get_public_params(self) -> dict:
        """
        获取解密所需的公开参数

        :return
            public_params(dict): {'mode': 加密类型}
        """
        return {'mode': self.mode}

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
    def decode(input: bytes, mode: str, iv: bytes, password: bytes) -> bytes:
        """
        AES 解密

        :param 
            input(bytes): 加密数据
            mode(str): 加密类型，可选：['ECB', 'CBC', 'CFB', 'OFB', 'CTR', 'OPENPGP', 'CCM', 'EAX', 'SIV', 'GCM', 'OCB']
            iv(bytes): 偏移值
            password(bytes): AES 密钥

        :return
            output(bytes): 原始数据
        """
        aes = AES.new(key=password, mode=ASE_MODES[mode], iv=iv)
        output = aes.decrypt(input)
        output = output.rstrip(b'\x00')
        return output
