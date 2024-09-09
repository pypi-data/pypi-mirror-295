# coding: utf-8

"""thriftpy hook.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import warnings

from swing.rpc_generator.plugins.thriftpy2 import hook

# from .errors import EulerDeprecatedWarning


class ThriftImporter(hook.ThriftImporter):
    def load_module(self, fullname):
        if not _thrift_imoprter_hook_installed_explicitly:
            msg = "import a thrift file without any configuration is deprecated in euler and will be removed in 2.0," +\
                  " please call euler.install_thrift_import_hook() explicitly before you import a thrift file."
            warnings.warn(msg)
        return super(ThriftImporter, self).load_module(fullname)


_imp = ThriftImporter()
_thrift_imoprter_hook_installed_explicitly = True


def _install_thrift_import_hook():
    global _imp
    sys.meta_path[:] = [x for x in sys.meta_path if _imp != x] + [_imp]


def install_thrift_import_hook():  # type: () -> None
    """ Install the thrift import hook, so that you can import a .thrift file directly.
    """
    global _thrift_imoprter_hook_installed_explicitly
    _thrift_imoprter_hook_installed_explicitly = True
    _install_thrift_import_hook()


def remove_thrift_import_hook():  # type: () -> None
    """ Remove the thrift import hook.
    """
    global _imp
    global _thrift_imoprter_hook_installed_explicitly
    sys.meta_path[:] = [x for x in sys.meta_path if _imp != x]
    _thrift_imoprter_hook_installed_explicitly = False
