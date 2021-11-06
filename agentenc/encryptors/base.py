import lzma


class BaseEncryptor:
    def __init__(self, **kwargs) -> None:
        '''
        Base Encryptor class
        '''
        pass

    def encrypt(self, input: bytes, **kwargs) -> bytes:
        '''
        encrypt func
        '''
        pass

    @staticmethod
    def decrypt(input: bytes, **kwargs) -> bytes:
        '''
        decrypt func
        '''
        pass

    @staticmethod
    def generate_keys(**kwargs) -> dict:
        '''
        generate keys
        '''
        pass

    @staticmethod
    def fn(mode: str):
        '''
        a decorator that adds compress param to a func

        param: 
            mode(str): decorator mode, ['encrypt', 'decrypt']

        return:
            warpper(func): warpper func
        '''
        def warpper(func):
            '''
            warpper func

            param:
                func(func): encrypt or decrypt func

            return:
                warpper(func): encrypt or decrypt func warpper
            '''
            if mode == 'encrypt':
                def warpper(obj, input: bytes, compress: bool = False, interval: int = 1, **kwargs) -> bytes:
                    '''
                    encrypt func warpper

                    param:
                        input(bytes len(input)[1-256^6]): input data
                        compress(bool: False): if compress data
                        interval(int: 1 [1-65535]): the interval of input data to encrypt, the recommended interval for text data is 1, means all are encrypted.
                        **kwargs: some other params of encrypt func

                    return:
                        output(bytes): output data
                    '''
                    assert isinstance(interval, int) and (1 <= interval <= 65535), 'interval should in 1-65535'
                    assert len(input) <= 256**6, 'input data is much large.'
                    output = func(obj, input[::interval])
                    length = len(output).to_bytes(6, 'big')
                    output = interval.to_bytes(2, 'big') + length + output + b''.join([v.to_bytes(1, 'big') for i, v in enumerate(input) if i % interval!=0])
                    if compress:
                        output = lzma.compress(output)
                    return output

            elif mode == 'decrypt':
                def warpper(input: bytes, compress: bool = False, **kwargs) -> bytes:
                    '''
                    decrypt func warpper

                    param:
                        input(bytes): input data
                        compress(bool: False): if compress data
                        head_len(int: 8): len of the head
                        **kwargs: some other params of encrypt func

                    return:
                        output(bytes): output data
                    '''
                    if compress:
                        input = lzma.decompress(input)
                    interval = int.from_bytes(input[:2], 'big')
                    length = int.from_bytes(input[2:8], 'big')
                    _output = func(input[8: length+8], **kwargs)
                    _data = input[length+8:]
                    output = b''
                    for i, v in enumerate(_output):
                        output += v.to_bytes(1, 'big') + _data[i*(interval-1):(i+1)*(interval-1)]

                    return output
            return warpper
        return warpper

    @classmethod
    def new(cls, **kwargs):
        '''
        new a Encryptor obj after generate keys

        param:
            **kwargs: some params of the Encryptor class

        return:
            obj(Encryptor): Encryptor obj
            params: params of Encryptor
            keys: random keys of Encryptor
        '''
        keys = cls.generate_keys()
        obj = cls(**keys, **kwargs)
        return obj, obj.params, keys
