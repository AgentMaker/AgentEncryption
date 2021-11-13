from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5, PKCS1_OAEP


RSA_MODES = {
    'PKCS1': PKCS1_v1_5,
    'PKCS1_OAEP': PKCS1_OAEP
}


def decrypt(input: bytes, bits: int, mode: str, private_key: bytes) -> bytes:
    '''
    RSA decrypt

    :param 
        input(bytes): input data
        bits(int): RSA bits
        mode(str): RSA modes, ['PKCS1', 'PKCS1_OAEP']
        private_key(bytes): RSA private key, b'-----BEGIN PRIVATE KEY-----...-----END PRIVATE KEY-----'

    :return
        output(bytes): output data
    '''
    rsa_key = RSA.importKey(private_key)
    cipher = RSA_MODES[mode].new(rsa_key)

    output = b''

    if mode == 'PKCS1':
        for i in range(0, len(input), bits//8):
            output += cipher.decrypt(input[i:i + bits//8], 'Decode error.')
    else:
        for i in range(0, len(input), bits//8):
            output += cipher.decrypt(input[i:i + bits//8])

    return output
