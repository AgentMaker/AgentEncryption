# Author: Acer Zhang
# Datetime: 2021/11/5 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import numpy as np
import paddle.inference as paddle_infer
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

# 创建 config
config = paddle_infer.Config(config)

# 根据 config 创建 predictor
predictor = paddle_infer.create_predictor(config)

# 获取输入的名称
input_names = predictor.get_input_names()
input_handle = predictor.get_input_handle(input_names[0])

# 设置输入
fake_input = np.array([1]).astype(np.float32)
input_handle.copy_from_cpu(fake_input)

# 运行predictor
predictor.run()

# 获取输出
output_names = predictor.get_output_names()
output_handle = predictor.get_output_handle(output_names[0])
output_data = output_handle.copy_to_cpu()  # numpy.ndarray类型
print("Output data size is {}".format(output_data.size))
print("Output data shape is {}".format(output_data.shape))

# 打开先前准备的测试结果数据
with open(SAVE_ENC_MODEL_PATH + "_one_test.txt", "r") as f:
    one = eval(f.read())

loss = abs(output_data - one)
print("LOSS:", loss)
if loss < 1e-5:
    print("误差较低，通过测试")
else:
    raise Exception("误差较高，请手动评估是否通过")
