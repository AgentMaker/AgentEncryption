import os
import json


def load(path: str, encoding: str = 'UTF-8') -> object:
    '''
    load data

    :param
        path(str): data path with file ext
        encoding(str: UTF-8): encoding of json file

    :return
        data([dict, bytes]): the json data in a dict or a bytes data
    '''
    assert os.path.isfile(path), 'Please check the path of file'
    if os.path.splitext(path)[1] == '.json':
        with open(path, 'r', encoding=encoding) as f:
            data = json.load(f)
    else:
        with open(path, 'rb') as f:
            data = f.read()
    return data
