# Author: Acer Zhang
# Datetime: 2021/10/27
# Copyright belongs to the author.
# Please indicate the source for reprinting.


class EncryptOp:
    def __init__(self, *args, **kwargs):
        pass

    def prepare(self, save_path):
        """
        定义准备流程
        """
        pass

    def get_params(self) -> dict:
        """
        客户端额外所需的解密信息，此处请勿返回任何公钥与私钥内容
        """
        pass

    def encode(self, text, *args, **kwargs) -> bytes:
        """
        定义加密流程
        """
        pass

    @staticmethod
    def decode(text, *args, **kwargs) -> bytes:
        """
        定义解密流程
        """
        pass
