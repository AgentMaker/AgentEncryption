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
                "datas": "ZfjW4CBOUp8u73BeT8aY9sIkWum...", 
                "params": {
                    "length": 128
                }
            }
            '''
        ```

