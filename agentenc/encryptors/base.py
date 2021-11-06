import math
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
        a decorator that adds ratio and compress params to a func

        param: 
            mode(str): decorator mode, ['encrypt', 'decrypt']

        return:
            warpper(func): warpper func
        '''
        def warpper(func):
            if mode == 'encrypt':
                def warpper(obj, input: bytes, ratio: int = 0.1, compress: bool = True, **kwargs) -> bytes:
                    '''
                    ratio 
                    '''
                    spilt_length = math.ceil(len(input) * ratio)
                    encrypt_datas = func(obj, input=input[:spilt_length])
                    encrypt_datas += b'##SPLIT##' + input[spilt_length:]
                    print(len(encrypt_datas))
                    if compress:
                        encrypt_datas = lzma.compress(encrypt_datas)
                    print(len(encrypt_datas))
                    return encrypt_datas
            elif mode == 'decrypt':
                def warpper(input: bytes, compress: bool = True, **kwargs) -> bytes:
                    '''
                    ratio 
                    '''
                    if compress:
                        input = lzma.decompress(input)
                    encrypt_input, noencrypt_input = input.split(b'##SPLIT##')
                    output = func(encrypt_input, **kwargs)
                    output += noencrypt_input
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
