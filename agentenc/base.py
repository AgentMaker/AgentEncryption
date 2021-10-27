# Author: Acer Zhang
# Datetime: 2021/10/27 
# Copyright belongs to the author.
# Please indicate the source for reprinting.
import os
import pickle

from paddle import inference

MODEL_FILE = "model.AgentEncryption"
PARAMS_FILE = "params.AgentEncryption"
OPT_FILE = "opt.AgentEncryption"


class BaseEncryptOp:
    def __init__(self, *args, **kwargs):
        pass

    def encoder(self, text, *args, **kwargs) -> bytes:
        """
        定义加密流程
        """
        pass

    def prepare(self, save_path):
        pass

    def get_param(self) -> dict:
        """
        客户端额外所需的解密信息，此处请勿返回任何公钥与私钥内容
        """
        pass

    @staticmethod
    def decoder(text, *args, **kwargs) -> bytes:
        """
        定义解密流程
        """
        pass


class BaseEncryptModelMaker:
    def __init__(self,
                 model_path,
                 param_path,
                 save_path,
                 encrypt_op: BaseEncryptOp):
        """
        模型加密基类 - 当前仅适配Combine模型
        :param model_path: 模型文件路径
        :param param_path: 参数文件路径
        :param save_path: 加密后模型文件保存路径
        :param encrypt_op: 加密相关OP
        """
        self.graph_path = model_path
        self.params_path = param_path
        self.save_path = save_path
        self.encrypt_op = encrypt_op

        self.graph = None
        self.params = None

    def pack(self) -> None:
        """
        序列化解密流程func
        """
        with open(os.path.join(self.save_path, OPT_FILE), "wb") as file:
            pickle.dump([self.encrypt_op.decoder, self.encrypt_op.get_param()], file)

    def load(self):
        with open(self.graph_path, "rb") as graph_file:
            self.graph = graph_file.read()

        with open(self.params_path, "rb") as params_file:
            self.params = params_file.read()

    def save(self):
        os.makedirs(self.save_path, exist_ok=True)
        with open(os.path.join(self.save_path, MODEL_FILE), "wb") as graph_file:
            graph_file.write(self.graph)

        with open(os.path.join(self.save_path, PARAMS_FILE), "wb") as params_file:
            params_file.write(self.params)

    def make(self):
        self.load()
        self.encrypt_op.prepare(self.save_path)
        self.graph = self.encrypt_op.encoder(self.graph)
        self.params = self.encrypt_op.encoder(self.params)
        self.pack()
        self.save()


class BaseEncryptConfigMaker:
    def __init__(self, load_path, config: inference.Config = None):
        self.load_path = load_path
        self.config = config

        # 占位符
        self.graph_path = None
        self.params_path = None
        self.op_path = None
        self.graph = None
        self.params = None

        self.op_func = None
        self.op_param = None

        # 准备工作
        self.prepare()

    def prepare(self):
        # 提前做个prepare，以后方便做拓展
        if not self.config:
            self.config = inference.Config()
        if not self.graph_path:
            self.graph_path = os.path.join(self.load_path, MODEL_FILE)
        if not self.params_path:
            self.params_path = os.path.join(self.load_path, PARAMS_FILE)
        if not self.op_path:
            self.op_path = os.path.join(self.load_path, OPT_FILE)

    def load(self):
        with open(self.graph_path, "rb") as graph_file:
            self.graph = graph_file.read()

        with open(self.params_path, "rb") as params_file:
            self.params = params_file.read()

        with open(self.op_path, "rb") as file:
            self.op_func, self.op_param = pickle.load(file)

    def make(self, **kwargs):
        self.load()
        self.graph = self.op_func(self.graph, self, **self.op_param, **kwargs)
        self.params = self.op_func(self.params, self, **self.op_param, **kwargs)
        self.config.set_model_buffer(self.graph, len(self.graph), self.params, len(self.params))
        # 返回加载情况
        return self.config.model_from_memory()

    @property
    def get_config(self):
        # 获取Config
        return self.config


EncryptConfigMaker = BaseEncryptConfigMaker
