from os import urandom
from Crypto.Cipher import AES

from .base import BaseEncryptor


# AES Mode Switch
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


class AESEncryptor(BaseEncryptor):
    def __init__(self, key: bytes, bits: int = 128, mode: str = 'ECB', **kwargs) -> None:
        """
        AES Encryptor

        :param 
            bits(int: 128): AES bits
            mode(str: ECB): AES mode, ['ECB', 'CBC', 'CFB', 'OFB', 'CTR', 'CCM', 'EAX', 'GCM', 'OCB']
            key(bytes: None): AES key, a length = (bits // 8) bytes key
            **kwargs: some other params, like 'iv', 'nonce' and so on
        """
        super().__init__()
        self.bytes = bits // 8
        self.mode = mode
        self.params = {
            'bits': bits,
            'mode': mode
        }
        self.aes = AES.new(
            key=key,
            mode=ASE_MODES[self.mode],
            **kwargs
        )

        if hasattr(self.aes, 'iv'):
            self.params['iv'] = self.aes.iv

        if hasattr(self.aes, 'nonce'):
            self.params['nonce'] = self.aes.nonce

    @BaseEncryptor.fn('encrypt')
    def encrypt(self, input: bytes) -> bytes:
        """
        AES encrypt

        :param 
            input(bytes): input data

        :return
            output(bytes): output data
        """
        count = len(input)
        pad = self.bytes - (count %
                            self.bytes) if count % self.bytes != 0 else 0
        input = input + pad.to_bytes(pad, 'big')
        output = self.aes.encrypt(input)
        return output

    @staticmethod
    @BaseEncryptor.fn('decrypt')
    def decrypt(input: bytes, mode: str, key: bytes, **kwargs) -> bytes:
        """
        AES decrypt

        :param 
            input(bytes): input data
            mode(str): AES mode, ['ECB', 'CBC', 'CFB', 'OFB', 'CTR', 'CCM', 'EAX', 'GCM', 'OCB']
            key(bytes: None): AES key, a length = (bits // 8) bytes key
            **kwargs: some other params, like 'iv', 'nonce' and so on

        :return
            output(bytes): output data
        """
        kwargs = {k: v for k, v in kwargs.items() if k in ['iv', 'nonce']}
        aes = AES.new(key=key, mode=ASE_MODES[mode], **kwargs)
        output = aes.decrypt(input)
        output = output[:-output[-1]]
        return output

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
