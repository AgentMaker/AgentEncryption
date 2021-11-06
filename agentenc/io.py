import os
import json
from typing import Union


def dump(obj: Union[dict, bytes], path: str, encoding: str = 'UTF-8') -> None:
    '''
    export data

    :param
        obj([dict, bytes]): data obj
        path(str): export path without file ext
        encoding(str: UTF-8): encoding of json file
    '''
    dir, _ = os.path.split(os.path.abspath(path))
    if not os.path.exists(dir):
        os.makedirs(dir)
    if isinstance(obj, bytes):
        with open(path+'.data', 'wb') as f:
            f.write(obj)
    elif isinstance(obj, dict):
        for k in obj.copy().keys():
            if isinstance(obj[k], bytes):
                v = obj.pop(k)
                with open(f'{path}.{k}', 'wb') as f:
                    f.write(v)
        if len(obj.keys()) > 0:
            with open(path+'.json', 'w', encoding=encoding) as f:
                json.dump(obj, f)
    else:
        obj_type = type(obj)
        raise ValueError(f'No support the {obj_type} object.')


def load(path: str, encoding: str = 'UTF-8'):
    '''
    load data

    :param
        path(str): data path with file ext
        encoding(str: UTF-8): encoding of json file
    '''
    assert os.path.isfile(path), 'Please check the path of file'
    if os.path.splitext(path)[1] == '.json':
        with open(path, 'r', encoding=encoding) as f:
            data = json.load(f)
    else:
        with open(path, 'rb') as f:
            data = f.read()
    return data
