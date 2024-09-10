"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/24 15:55
@Author: xingyun
"""


class IDict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


def dict2obj(dict_obj):
    if not isinstance(dict_obj, dict):
        return dict_obj
    d = IDict()
    for k, v in dict_obj.items():
        d[k] = dict2obj(v)
    return d
