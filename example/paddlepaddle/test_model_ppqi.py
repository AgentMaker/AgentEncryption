# Author: Acer Zhang
# Datetime: 2021/11/5 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import numpy as np

from ppqi import InferenceModel
from agentenc import Encryptor

SAVE_ENC_MODEL_PATH = "./model/enc_model"
SAVE_ENC_MODEL_FILE_PATH = SAVE_ENC_MODEL_PATH + ".EncPdModel"
# 读取私钥
private_key = open('key.PRIVATE', 'rb').read()

# 使用解密函数对文件进行解密
config = Encryptor.decode(
    inp=SAVE_ENC_MODEL_FILE_PATH,
    private_key=private_key
)

# 加载推理模型
model = InferenceModel(config)
model.eval()

# 准备数据
inputs = np.array([1]).astype(np.float32)

# 前向计算
outputs = model(inputs)

# 打开先前准备的测试结果数据
with open(SAVE_ENC_MODEL_PATH + "_one_test.txt", "r") as f:
    one = eval(f.read())

loss = abs(outputs - one)
print("LOSS:", loss)
if loss < 1e-5:
    print("误差较低，通过测试")
else:
    raise Exception("误差较高，请手动评估是否通过")
