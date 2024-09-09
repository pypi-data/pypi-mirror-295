"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/28 17:00
@Author: xingyun
"""

import functools

rpc_deps = {}


def xray_trace_rpc(psm, rpc):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            key = psm
            if psm == "":
                key = "Unknown"
            if key not in rpc_deps:
                rpc_deps[key] = {rpc}
            else:
                rpc_deps[key].add(rpc)
            return func(*args, **kw)

        return wrapper

    return decorator
