# AgentEncryption
飞桨模型加密库 - EAP阶段  
在分发加密模型时，请务必进行不限于以下的操作方可避免轻易破解    
- [x] 加密深度学习框架以及其相关的Python库，至少为pyd格式
- [x] 加密AgentEncryption库，至少为pyd格式
- [x] 限制用户只能使用你提供的Python环境



> 飞桨推理模型加密可参考[从内存中加载加密飞桨推理模型](./example/paddlepaddle)
> 1. [加密飞桨模型](./example/paddlepaddle/make_model.py)
> 2. [借助PPQI推理加密的飞桨模型](./example/paddlepaddle/test_model_ppqi.py)
> 3. [借助PaddleInference推理加密的飞桨模型](./example/paddlepaddle/test_model_paddleinference.py)

## 快速使用
* 如下是几个简单的示例代码：
    * 数据加密：

        ```python
        # 导入 RSA 加密器
        from agentenc import RSAEncryptor

        # 初始化 RSA 加密器
        encryptor = RSAEncryptor(bits=1024)

        # 构建原始数据
        pure_data = {
            'int': 100,
            'float': 0.01,
            'str': 'hello',
            'list': [100, 0.01, 'hello']
        }

        # 数据加密
        key = encryptor.encode(
            input=pure_data, 
            output='out', 
            format='pkl', 
            keys_saving_path='key'
        )

        # 打印随机生成的密钥
        print(key) 

        '''
        {
            'private_key': b'-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQDQq3mzdfDYjg8ool1Jl5WrmFAkJWarokIQAzq/3wT+cbNUy/zv\nqxHCn7bYsifvx5nLnfCL7cm3BVygnB4clP8p6EAlO8KcocC/6WfCyTW5gw23z5Tc\ntzSzAERtNTGwDst3RAnEDeJ2crNi/xSs2Wa6k1bNkxNFUehEd4ExpYFwLQIDAQAB\nAoGAWmYG9aOBANfeIkzgnBqSyQFVqqsXRQConPZBM9EigTZxqakrfQq/yXBWjp7z\npTFz452bEYukqOimPaAUfW5g8ZYxndN2G1ctWMPg3KrJ++7FYFJJhJ223IOmSmB4\nKf2FyVjBNUTzKchBdxHcLqAQX1DNXnWrJ5cWc2pS0olz+BMCQQDTZ8hqIT1UPclk\noPTX6gC+874D+GNa5r4CsMMiUZNrN7hCXEwZJ+3kR14vcJkDd2QVg8cR6VSxP9Vg\nBg5XuD2jAkEA/K/3mtKMDhX5HjNUfoBzLBSJreAVMOcGGrLCLFob+8t64456SQ8I\nOKABsocpKaRp+s3loi6obGoRwIQ5PBTX7wJBAMp60pfj8kunSidZimjqtYAvEEXZ\nN8Au1Lra9mr+WwYMPi1BHZnShqVoPauOWt/ZEEETEC31n6qNCx+HbWFTE6UCQEfF\n16ezPDLYDO2GGO7hn1Ua9ExeBMbiJ/q3Ya3lXmNz1ZEDLDrKOUSUNkc2WvvIBo5F\no38gj5hTvH0ZUYR+SyMCQEnnTVZXhtU7jtyOfEXsTqUtZIVo01sJ5SoekGrnZ0Ht\n8PxyjyOc5IFWieKGUfZQ3ZdKDm95dvAyKpkDa8tqMCM=\n-----END RSA PRIVATE KEY-----', 
            'public_key': b'-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDQq3mzdfDYjg8ool1Jl5WrmFAk\nJWarokIQAzq/3wT+cbNUy/zvqxHCn7bYsifvx5nLnfCL7cm3BVygnB4clP8p6EAl\nO8KcocC/6WfCyTW5gw23z5TctzSzAERtNTGwDst3RAnEDeJ2crNi/xSs2Wa6k1bN\nkxNFUehEd4ExpYFwLQIDAQAB\n-----END PUBLIC KEY-----'
        }
        '''

        # 使用解密函数对文件进行解密
        data = RSAEncryptor.decode(
            inp='out.pkl', 
            private_key=key['private_key']
        )

        # 输入与输出数据对比
        print(data == pure_data) 
        
        '''
        True
        '''
        ```

    * 数据解密：

        ```python
        # 导入基础加密器
        from agentenc import Encryptor

        # 读取私钥
        private_key = open('key.PRIVATE', 'rb').read() 
        
        # 使用解密函数对文件进行解密
        data = Encryptor.decode(
            inp='out.pkl', 
            private_key=private_key
        )

        # 输入与输出数据对比
        print(data)

        '''
        {
            'int': 100, 
            'float': 0.01, 
            'str': 'hello', 
            'list': [100, 0.01, 'hello']
        }
        '''
        ```
