import os

from lced_utils.buffer_utils import get_project_connect, iter_set_connect_info
from lced_utils.str_utils import to_camel_case


class Connect:
    _pre_url = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

    @staticmethod
    def get_class(key):
        module_name = f"{key}_server"
        full_name = f"{Connect._pre_url}.{key}.{module_name}"
        from_obj = to_camel_case(module_name, is_pascal=True)
        module_handler = getattr(__import__(full_name, fromlist=from_obj), from_obj)
        return module_handler

    @staticmethod
    def execute_connect_handler(obj, info, connect_name, tag):
        res = obj(info).get_handler()
        iter_set_connect_info(connect_name, {tag: res})

    @staticmethod
    def run():
        for key, val in get_project_connect().items():
            for k, v in val.items():
                if v.get("enable"):
                    obj = Connect.get_class(key)
                    Connect.execute_connect_handler(obj, v, key, k)
