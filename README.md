# AgentEncryption
飞桨模型加密库 - EAP阶段  

## 快速使用
* 如下是几个简单的示例代码：
    * Python 格式加密：

        ```python
        # 导入 RSA 加密器
        from agentenc import RSAEncryptor

        # 初始化 RSA 加密器
        encryptor = RSAEncryptor(bits=1024)

        # 使用加密器进行加密
        pure_data = {
            'pdmodel': open('test/sample_model/model1.pdmodel', 'rb').read(),
            'pdiparams': open('test/sample_model/model1.pdiparams', 'rb').read()
        }
        encryptor.encode(input=pure_data, output='out', with_decode=True)

        # 使用解密函数对文件进行解密
        data = RSAEncryptor.decode(input='out.agt', private_pem=encryptor.encrypt_op.private_pem)

        # 输入与输出数据对比
        print(data == pure_data) # True
        ```

    * Json 格式加密：

        ```python
        # 导入 RSA 加密器
        from agentenc import RSAEncryptor

        # 初始化 RSA 加密器
        encryptor = RSAEncryptor(bits=1024)

        # 使用加密器进行加密
        pure_data = {
            'pdmodel': open('test/sample_model/model1.pdmodel', 'rb').read(),
            'pdiparams': open('test/sample_model/model1.pdiparams', 'rb').read()
        }
        encryptor.encode(input=pure_data, output='out', with_decode=False)

        # 使用解密函数对文件进行解密
        data = RSAEncryptor.decode(input='out.json', private_pem=encryptor.encrypt_op.private_pem)

        # 输入与输出数据对比
        print(data == pure_data) # True

        '''
        # out.json
        {
            "datas": "fmgyRDvtC+LE449sA...", 
            "params": {
                "length": 128
            }
        }
        '''
        ```

    * 通过加密器和加密算子搭配进行使

        ```python
        # 导入 RSA 加密算子和加密器
        from agentenc import Encryptor
        from agentenc.ops import RSAEncryptOp

        # 选择并初始化使用的加密算子
        encrypt_op = RSAEncryptOp(bits=1024)

        # 使用加密算子初始化加密器
        encryptor = Encryptor(encrypt_op=encrypt_op)

        # 使用加密器进行加密
        pure_data = {
            'pdmodel': open('test/sample_model/model1.pdmodel', 'rb').read(),
            'pdiparams': open('test/sample_model/model1.pdiparams', 'rb').read()
        }
        encryptor.encode(input=pure_data, output='out')

        # 使用解密函数对文件进行解密
        data = Encryptor.decode(input='out.agt', private_pem=encryptor.encrypt_op.private_pem)

        # 输入与输出数据对比
        print(data==pure_data) # True
        ```
