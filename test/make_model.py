# Author: Acer Zhang
# Datetime: 2021/10/27 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

import paddle

fc = paddle.nn.Linear(1, 1)
# -1.68187106
print(fc.weight, fc.bias)

input_1 = paddle.static.InputSpec(shape=[-1, 1], name="input_1")
paddle.jit.save(fc, path="./sample_model/model1", input_spec=[input_1])

test_ipt = paddle.to_tensor([1.], dtype="float32")
out = fc(test_ipt).numpy()
with open("./sample_model/one_test.txt", "w") as f:
    f.write(str(out))
print(out)
