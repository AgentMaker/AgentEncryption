from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


def decrypt(input: bytes, bits: int, private_key: bytes) -> bytes:
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
