"""
coding:utf-8
@Software: PyCharm
@Time: 2024/4/28 16:44
@Author: xingyun
"""
from __future__ import absolute_import

# coding: utf-8

from __future__ import division
from __future__ import print_function

import os

from ..thrift_hook import hook

if 'EULER_DISABLE_IMPORT_HOOK' not in os.environ:
    hook._install_thrift_import_hook()

from .__version__ import __version__  # NOQA
from .hook import install_thrift_import_hook, remove_thrift_import_hook  # NOQA


__all__ = ["install_thrift_import_hook", "remove_thrift_import_hook"]
