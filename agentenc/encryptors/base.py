class BaseEncryptor:
    params: dict  # dict of the Encryptor params
    keys: dict  # dict of the Encryptor keys

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

    @classmethod
    def new(cls, **kwargs) -> tuple:
        '''
        new a Encryptor obj after generate keys

        param:
            **kwargs: some params of the Encryptor class

        return:
            obj(Encryptor): Encryptor obj
            params: params of Encryptor
            keys: random keys of Encryptor
        '''
        obj = cls(**kwargs)
        return obj, obj.params, obj.keys
