# AgentEncryption
飞桨模型加密库 - EAP阶段  

## 快速使用
* 如下是几个简单的示例代码：

    ```python
    from agentenc import RSAEncryptor

    # 初始化 RSA 加密器
    encryptor = RSAEncryptor()

    # 使用加密器进行加密
    pure_data = {
        'pdmodel': open('test/sample_model/model1.pdmodel', 'rb').read(),
        'pdiparams': open('test/sample_model/model1.pdiparams', 'rb').read()
    }
    output = 'out.agt'
    encryptor.encode(pure_data, output)

    # 使用解密函数对文件进行解密
    data = RSAEncryptor.decode(output, encryptor.encrypt_op.private_pem)

    # 输入与输出数据对比
    print(data == pure_data)
    ```

    ```python
    from agentenc import Encryptor
    from agentenc.ops import RSAEncryptOp

    # 选择并初始化使用的加密算子
    encrypt_op = RSAEncryptOp()

    # 使用加密算子初始化加密器
    encryptor = Encryptor(encrypt_op)

    # 使用加密器进行加密
    pure_data = {
        'pdmodel': open('test/sample_model/model1.pdmodel', 'rb').read(),
        'pdiparams': open('test/sample_model/model1.pdiparams', 'rb').read()
    }
    output = 'out.agt'
    encryptor.encode(pure_data, output)

    # 使用解密函数对文件进行解密
    data = Encryptor.decode(output, private_pem=encryptor.encrypt_op.private_pem)

    # 输入与输出数据对比
    print(data==pure_data)
    ```