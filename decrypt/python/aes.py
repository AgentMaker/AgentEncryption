from Crypto.Cipher import AES

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
    aes = AES.new(key=key, mode=ASE_MODES[mode], **kwargs)
    output = aes.decrypt(input)
    pad = output[-1]
    return output[:-pad]
