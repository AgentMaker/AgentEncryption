# AgentEncryption
一个简单方便的加密库

## 代码使用
* 快速使用

    ```python
    # 导入 AES 加密器
    from agentenc import AESEncryptor

    # 创建一个加密器
    aes = AESEncryptor(bits=128, mode='ECB')

    # 打印参数信息
    print(aes.params)
    '''
    {'bits': 128, 'mode': 'ECB'}
    '''

    # 打印密钥信息
    print(aes.keys)
    '''
    {'key': b'9\xf1bu\xe8c`]\x98\x8e\xd5#d\x19\x99\x05'}
    '''

    # 使用一个字符串的 Bytes 数据进行加密测试
    input_data = b'Hello Encryptor.'

    # 使用 AES 加密器对输入数据进行加密
    output_data = aes.encrypt(input_data)

    # 打印加密后的数据
    print(output_data)
    '''
    b"\xfd7zXZ\x00\x00\x04...\x01\x00\x00\x00\x00\x04YZ"
    '''

    # 使用 AES 解密函数对加密数据进行解密
    # 解密函数需要使用上面返回的加密器参数和密钥信息
    _input_data = AESEncryptor.decrypt(output_data, **aes.params, **aes.keys)

    # 打印解密数据
    print(_input_data)
    '''
    b'Hello Encryptor.'
    '''

    # 对比加解密前后的数据
    print(_input_data==input_data)
    '''
    True
    '''
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
    from agentenc import AESEncryptor, dump

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
    from agentenc import AESEncryptor, load

    # 加载密钥
    key = load('export/KEY.key')

    # 使用自定义的 key 初始化加密器
    aes = AESEncryptor(bits=128, mode='ECB', key=key)

    # 获取参数信息
    params = aes.params
    ```
