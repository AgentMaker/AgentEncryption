# Author: Acer Zhang
# Datetime: 2021/10/27
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import pickle


class BaseEncryptOp:
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


class BaseEncrypt:
    def __init__(self,
                 encrypt_op: BaseEncryptOp):
        """
        资源文件加密基类
        :param encrypt_op: 加密相关OP
        """
        self.encrypt_op = encrypt_op

    def encode(self, input: dict, output: str):
        encrypt_datas = self.encrypt_op.encode(pickle.dumps(input))
        with open(output, "wb") as file:
            pickle.dump({
                'datas': encrypt_datas,
                'params': self.encrypt_op.get_params(),
                'decode': self.encrypt_op.decode
            }, file)

    @staticmethod
    def decode(input: str, **kwargs):
        with open(input, "rb") as file:
            encrypt_package = pickle.load(file)
        params = encrypt_package['params']
        encrypt_datas = encrypt_package['datas']
        decode = encrypt_package['decode']
        pure_datas = decode(encrypt_datas, **kwargs, **params)
        output = pickle.loads(pure_datas)
        return output
