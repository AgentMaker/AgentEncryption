from os import urandom
from Crypto.Cipher import AES

from .base import BaseEncryptor


class AESEncryptor(BaseEncryptor):
    ASE_MODES = {
        'ECB': AES.MODE_ECB,
        'CBC': AES.MODE_CBC,
        'CFB': AES.MODE_CFB,
        'OFB': AES.MODE_OFB,
        'CTR': AES.MODE_CTR,
        'CCM': AES.MODE_CCM,
        'EAX': AES.MODE_EAX,
        'GCM': AES.MODE_GCM,
        'OCB': AES.MODE_OCB
    }
    '''
    AES modes: ['ECB', 'CBC', 'CFB', 'OFB', 'CTR', 'CCM', 'EAX', 'GCM', 'OCB']
    '''

    def __init__(self, bits: int = 128, mode: str = 'ECB', key: bytes = None, **kwargs) -> None:
        '''
        AES Encryptor

        :param 
            bits(int: 128): AES bits
            mode(str: ECB): AES mode, ['ECB', 'CBC', 'CFB', 'OFB', 'CTR', 'CCM', 'EAX', 'GCM', 'OCB']
            key(bytes: None): AES key, a length = (bits // 8) bytes key
            **kwargs: some other params, like 'iv', 'nonce'
        '''
        super().__init__()
        self.bytes = bits // 8
        self.mode = mode
        self.params = {
            'bits': bits,
            'mode': mode
        }

        self.keys = self.generate_keys(
            bits=bits) if key is None else {'key': key}

        self.aes = AES.new(
            key=self.keys['key'],
            mode=self.ASE_MODES[self.mode],
            **kwargs
        )

        if hasattr(self.aes, 'iv'):
            self.params['iv'] = self.aes.iv

        if hasattr(self.aes, 'nonce'):
            self.params['nonce'] = self.aes.nonce

    def encrypt(self, input: bytes) -> bytes:
        '''
        AES encrypt

        :param 
            input(bytes): input data

        :return
            output(bytes): output data
        '''
        length = len(input)
        amount_to_pad = AES.block_size - (length % AES.block_size)
        if amount_to_pad == 0:
            amount_to_pad = AES.block_size
        pad = amount_to_pad.to_bytes(amount_to_pad, 'big')
        input += pad
        output = self.aes.encrypt(input)
        return output

    @staticmethod
    def decrypt(input: bytes, mode: str, key: bytes, **kwargs) -> bytes:
        '''
        AES decrypt

        :param 
            input(bytes): input data
            mode(str): AES mode, ['ECB', 'CBC', 'CFB', 'OFB', 'CTR', 'CCM', 'EAX', 'GCM', 'OCB']
            key(bytes: None): AES key, a length = (bits // 8) bytes key
            **kwargs: some other params, like 'iv', 'nonce' and so on

        :return
            output(bytes): output data
        '''
        kwargs = {k: v for k, v in kwargs.items() if k in ['iv', 'nonce']}
        aes = AES.new(key=key, mode=AESEncryptor.ASE_MODES[mode], **kwargs)
        output = aes.decrypt(input)
        pad = output[-1]
        return output[:-pad]

    @staticmethod
    def generate_keys(bits: int = 128) -> dict:
        '''
        generate AES key

        :param 
            bits(int: 128): AES bits

        :return
            output(dict): a dict of AES key, {'key': key}
        '''
        return {'key': urandom(bits // 8)}
