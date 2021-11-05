# Author: Acer Zhang
# Datetime: 2021/11/5 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import paddle
# 导入 RSA 加密器
from agentenc import RSAEncryptor

SAVE_ORI_MODEL_PATH = "./model/ori_model"
SAVE_ENC_MODEL_PATH = "./model/enc_model"

"""
制作一个简单的模型
"""

# 模拟一个线性层组成的模型
fc = paddle.nn.Linear(1, 1)
# 转静态图
input_1 = paddle.static.InputSpec(shape=[-1, 1], name="input_1")
# 保存模型
paddle.jit.save(fc, path=SAVE_ORI_MODEL_PATH, input_spec=[input_1])

# 输入一个常量，查看结果
test_ipt = paddle.to_tensor([1.], dtype="float32")
out = fc(test_ipt).numpy()
# 保持该结果，用于解密后的验证
with open(SAVE_ENC_MODEL_PATH + "_one_test.txt", "w") as f:
    f.write(str(out))
print("当输入1时，程序应得到的结果为：", out)

"""
加密模型
"""

# 初始化 RSA 加密器
encryptor = RSAEncryptor(bits=1024)

# 数据加密
key = encryptor.encode(
    inp=SAVE_ORI_MODEL_PATH,
    output=SAVE_ENC_MODEL_PATH,
    format='pdmodel',
    keys_saving_path='key'
)
print("加密完毕")
