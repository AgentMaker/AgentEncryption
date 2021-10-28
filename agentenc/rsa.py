# Author: Acer Zhang
# Datetime: 2021/10/27 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

from agentenc.op import SampleRSAOp
from agentenc.base import BaseEncrypt


class RSAEncrypt(BaseEncrypt):
    def __init__(self,
                 bits=1024):
        super(RSAEncrypt, self).__init__(encrypt_op=SampleRSAOp(bits))

    @staticmethod
    def decode(input: str, private_pem: bytes):
        return BaseEncrypt.decode(input, private_pem=private_pem)