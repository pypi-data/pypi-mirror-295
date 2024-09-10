import os

from lced_variables.dict_var import SingletonDict


class Connect:
    _pre_url = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self, *args, **kwargs):
        self.connect_buffer = SingletonDict()["config_info"].get("CONNECT", {})

    @staticmethod
    def get_class(key):
        name = f"{Connect._pre_url}.{key}.{key}_server"
        fromobj = f"{key}_execute"
        return getattr(__import__(name, fromlist=fromobj), fromobj)

    def run(self, *args, **kwargs):
        for key, val in self.connect_buffer.items():
            for k, v in val.items():
                if v.get("enable"):
                    c_tag = f"{key}_{k}"
                    Connect.get_class(key)(v, c_tag)
