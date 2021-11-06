# AgentEncryption
一个简单方便的加密库

## 代码使用
* 快速使用

    ```python
    # 导入 AES 加密器
    from agentenc import AESEncryptor

    # 使用 Encryptor 的 new() 方法
    # 会自动完成随机密钥生成和加密器初始化
    # 并返回加密器实例、加密器的参数以及生成的密钥信息
    # new() 方法的更多参数说明请参考对应的 Encryptor
    aes, params, keys = AESEncryptor.new(bits=128, mode='ECB')

    # 打印参数信息
    print(params)

    # 打印密钥信息
    print(keys)

    # 使用一个字符串的 Bytes 数据进行加密测试
    input_data = b'Hello Encryptor.'

    # 使用 AES 加密器对输入数据进行加密
    # ratio(0.0-1.0) 参数控制加密的数据比例，参数越大压缩比例越大
    # compress 参数表示是否对数据进行压缩处理 
    output_data = aes.encrypt(input_data, ratio=0.1, compress=True)

    # 打印加密后的数据
    print(output_data)

    # 使用 AES 解密函数对加密数据进行解密
    # 解密函数需要使用上面返回的加密器参数和密钥信息
    _input_data = AESEncryptor.decrypt(output_data, **params, **keys)

    # 打印解密数据
    print(_input_data)

    # 对比加解密前后的数据
    print(_input_data==input_data)
    ```

* 导出与加载

    ```python
    from agentenc import dump, load

    # 使用 dump 方法进行数据、密钥和参数信息的导出
    # 输入的对象必须为字典或 Bytes
    # 设置的 path 无需包含文件后缀
    # Bytes -> {path}.data
    # Dict 中的 Bytes Vaule -> {path}.{Key in Dict}
    # 其余的 Dict -> {path}.json
    dump(obj, path)

    # 加载导出的数据
    # path 需要填写完整路径包含文件后缀
    obj = load(path)
    ```

* 生成密钥：

    ```python
    import os
    from agentenc import AESEncryptor, dump, load

    # 随机生成密钥
    keys = AESEncryptor.generate_keys()

    # 打印密钥信息
    print(keys)
    '''
    {'key': b'\xb0#\xb1\x85\x81\xff\x15\x9fz/m\x96X\xd2\x1c\xe9'}
    '''

    # 导出密钥
    dump(keys, 'export/KEY')

    # 列出文件
    print(os.listdir('export'))
    '''
    ['KEY.key']
    '''
    ```

* 自定义密钥加密：

    ```python
    # 导入 AES 加密器
    from agentenc import AESEncryptor

    # 加载密钥
    key = load('export/KEY.key')

    # 使用自定义的 key 初始化加密器
    aes = AESEncryptor(bits=128, mode='ECB', key=key)

    # 获取参数信息
    params = aes.params
    ```
