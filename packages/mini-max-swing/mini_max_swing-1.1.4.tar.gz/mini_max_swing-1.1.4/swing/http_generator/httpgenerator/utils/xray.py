"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/28 17:25
@Author: xingyun
"""

import functools

http_deps = {}


def xray_trace(psm, path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            key = psm
            if psm == "":
                key = "Unknown"
            if key not in http_deps:
                http_deps[key] = {path}
            else:
                http_deps[key].add(path)
            return func(*args, **kw)

        return wrapper

    return decorator
