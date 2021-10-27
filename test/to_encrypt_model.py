# Author: Acer Zhang
# Datetime: 2021/10/27 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

from agentenc.rsa import RSAEncryptModelMaker

maker = RSAEncryptModelMaker(model_path="./sample_model/model1.pdmodel",
                             param_path="./sample_model/model1.pdiparams",
                             save_path="./model_out")
maker.make()
