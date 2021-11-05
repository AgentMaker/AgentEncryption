# Author: Acer Zhang
# Datetime: 2021/10/27
# Copyright belongs to the author.
# Please indicate the source for reprinting.

from os import urandom
from Crypto.Cipher import AES

from agentenc.ops import EncryptOp


IV_FILE = "IV"
KEY_FILE = "KEY"


# AES Mode Switch
ASE_MODES = {
    'ECB': AES.MODE_ECB,
    'CBC': AES.MODE_CBC,
    'CFB': AES.MODE_CFB,
    'OFB': AES.MODE_OFB,
    'CTR': AES.MODE_CTR,
    'CCM': AES.MODE_CCM,
    'EAX': AES.MODE_EAX,
    'GCM': AES.MODE_GCM,
    'OCB': AES.MODE_OCB
}


class AESEncryptOp(EncryptOp):
    def __init__(self, bits: int = 128, mode: str = 'ECB', key: bytes = None, **kwargs):
        """
        AES 加密算子

        :param 
            bits(int: 128): 加密 bit 数
            mode(str: ECB): 加密类型，可选：['ECB', 'CBC', 'CFB', 'OFB', 'CTR', 'CCM', 'EAX', 'GCM', 'OCB']
            key(bytes: None): AES 密钥，长度为 (bits // 8) bytes ，默认随机生成
            **kwargs: 一些其他的加密参数，如 iv, nonce 等
        """
        super().__init__()
        self.length = bits // 8
        self.mode = mode

        if key is not None:
            self.key = key
        else:
            self.key = urandom(self.length)

        self.aes = AES.new(
            key=self.key,
            mode=ASE_MODES[self.mode],
            **kwargs
        )

    def get_private_params(self, save_path: str = None) -> dict:
        """
        获取并保存密钥

        :param 
            save_path(str: None): 密钥保存目录

        :return
            private_params(dict): {'key': AES 密钥}

        :save file details
            "{save_path}.key": AES 密钥
        """
        if save_path:
            with open(f'{save_path}.{KEY_FILE}', "wb") as f:
                f.write(self.key)

        return {
            'key': self.key
        }

    def get_public_params(self) -> dict:
        """
        获取解密所需的公开参数

        :return
            public_params(dict): {'mode': 加密类型}
        """

        if hasattr(self.aes, 'iv'):
            return {
                'mode': self.mode,
                'iv': self.aes.iv
            }
        elif hasattr(self.aes, 'nonce'):
            return {
                'mode': self.mode,
                'nonce': self.aes.nonce
            }
        else:
            return {
                'mode': self.mode
            }

    def encode(self, input: bytes) -> bytes:
        """
        AES 加密

        :param 
            inp(bytes): 输入数据

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
    def decode(input: bytes, mode: str, key: bytes, **kwargs) -> bytes:
        """
        AES 解密

        :param 
            inp(bytes): 加密数据
            mode(str): 加密类型，可选：['ECB', 'CBC', 'CFB', 'OFB', 'CTR', 'CCM', 'EAX', 'GCM', 'OCB']
            key(bytes): AES 密钥
            **kwargs: 一些其他的加密参数，如 iv, nonce 等

        :return
            output(bytes): 原始数据
        """
        aes = AES.new(key=key, mode=ASE_MODES[mode], **kwargs)
        output = aes.decrypt(input)
        output = output.rstrip(b'\x00')
        return output
