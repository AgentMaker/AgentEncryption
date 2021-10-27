# Author: Acer Zhang
# Datetime: 2021/10/27 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import numpy as np
from ppqi import InferenceModel

NO_ENC = "./sample_model/model1"
ENC = "./model_out/model"
# 读取记录的前向数据，为后续推理做对比
with open("./sample_model/one_test.txt", "r") as f:
    one = eval(f.read())

# 加载推理模型
model = InferenceModel(modelpath=ENC)
model.eval()

# 准备数据
inputs = np.array([1]).astype(np.float32)

# 前向计算
outputs = model(inputs)

loss = abs(outputs - one)
print("LOSS:", loss)
if loss < 1e-5:
    print("误差较低，通过测试")
else:
    raise Exception("误差较高，请手动评估是否通过")
