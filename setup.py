# Author: Acer Zhang
# Datetime: 2021/10/27 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

from setuptools import setup
from setuptools import find_packages

__version__ = "0.1"

setup(
    name='AgentEnc',
    version=__version__,
    packages=find_packages(),
    url='https://github.com/AgentMaker/AgentEncryption',
    license='Apache2',
    author='GT-ZhangAcer',
    author_email='zhangacer@foxmail.com',
    description='飞桨模型加密库',
    install_requires=["ppqi",
                      "pycryptodome"],
    python_requires='>3.5',
    include_package_data=True,
)
