from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

from .base import BaseEncryptor


class RSAEncryptor(BaseEncryptor):
    def __init__(self, bits: int = 1024, public_key: bytes = None) -> None:
        '''
        RSA Encryptor

        :param
            bits(int: 1024): RSA bits
            public_key(bytes: None): RSA public key, b'-----BEGIN PUBLIC KEY-----...-----END PUBLIC KEY-----'
        '''
        super().__init__()
        self.bits = bits
        self.bytes = bits // 8 - 11
        self.params = {'bits': bits}
        self.keys = self.generate_keys(bits=bits) if public_key is None else {
            'public_key': public_key}

        rsa_key = RSA.importKey(self.keys['public_key'])
        self.cipher = PKCS1_v1_5.new(rsa_key)

    def encrypt(self, input: bytes) -> bytes:
        '''
        RSA encrypt

        :param
            input(bytes): input data

        :return
            output(bytes): output data
        '''
        output = b''
        for i in range(0, len(input), self.bytes):
            output += self.cipher.encrypt(input[i:i + self.bytes])
        return output

    @staticmethod
    def decrypt(input: bytes, bits: int, private_key: bytes, **kwargs) -> bytes:
        '''
        RSA decrypt

        :param 
            input(bytes): input data
            length(int): length of encryption
            private_key(bytes): RSA private key, b'-----BEGIN PRIVATE KEY-----...-----END PRIVATE KEY-----'

        :return
            output(bytes): output data
        '''
        rsa_key = RSA.importKey(private_key)
        cipher = PKCS1_v1_5.new(rsa_key)

        output = b''
        for i in range(0, len(input), bits//8):
            output += cipher.decrypt(input[i:i + bits//8], 'Decode error.')

        return output

    @staticmethod
    def generate_keys(bits: int = 1024) -> dict:
        '''
        generate RSA private and public keys

        :param 
            bits(int: 1024): RSA bits

        :return
            output(dict): a dict of RSA private and public keys, {'private_key': private_key, 'public_key': public_key}
        '''
        rsa = RSA.generate(bits, Random.new().read)
        private_key = rsa.exportKey()
        public_key = rsa.publickey().exportKey()
        return {
            'private_key': private_key,
            'public_key': public_key
        }

    @classmethod
    def new(cls: BaseEncryptor, bits: int = 1024, public_key: bytes = None) -> tuple:
        '''
        new a RSA Encryptor

        :param 
            bits(int: 1024): RSA bits
            public_key(bytes: None): RSA public key, b'-----BEGIN PUBLIC KEY-----...-----END PUBLIC KEY-----'

        return:
            obj(RSAEncryptor): RSA Encryptor obj
            params(dict): params of RSA Encryptor
            keys(dict): random keys of RSA Encryptor
        '''
        return super().new(bits=bits, public_key=public_key)
