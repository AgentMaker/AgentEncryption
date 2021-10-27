# Author: Acer Zhang
# Datetime: 2021/10/27 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

from agentenc.base import BaseEncryptModelMaker
from agentenc.op import RSAOp


class RSAEncryptModelMaker(BaseEncryptModelMaker):
    def __init__(self,
                 model_path,
                 param_path,
                 save_path,
                 bits=1024):
        super().__init__(model_path,
                         param_path,
                         save_path,
                         encrypt_op=RSAOp(bits))
