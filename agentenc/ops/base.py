# Author: Acer Zhang
# Datetime: 2021/10/27
# Copyright belongs to the author.
# Please indicate the source for reprinting.


class EncryptOp:
    def __init__(self):
        '''
        加密算子基类
        '''
        pass

    def get_private_params(self, **kwargs) -> dict:
        """
        获取隐私参数并储存，如获取并保存密钥等信息
        """
        pass

    def get_public_params(self, **kwargs) -> dict:
        """
        客户端额外所需的解密信息，此处请勿返回任何公钥与私钥内容
        """
        pass

    def encode(self, input: bytes, **kwargs) -> bytes:
        """
        定义加密流程
        """
        pass

    @staticmethod
    def decode(input: bytes, **kwargs) -> bytes:
        """
        定义解密流程
        """
        pass
