# coding: utf-8

"""Error types of euler. Most function in euler will throw errors in this module if it failed.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


UNKNOWN_METHOD_ERROR_CODE = 1

UNKNOWN_ERROR_CODE = 100
REMOTE_OR_NET_ERROR_CODE = 119


class EulerError(Exception):
    def __init__(self, error_code=UNKNOWN_ERROR_CODE, message="unknown euler error"):
        super(EulerError, self).__init__('EulerError, error_code: %d, message: %s' % (error_code, message))
        self.error_code = error_code
        self.message = message


class MethodNotFoundError(EulerError):
    def __init__(self, **kwargs):
        message = kwargs.pop('message', "unknown method")
        if kwargs:
            raise TypeError('unexcept arguments: ' + kwargs.keys()[0])
        super(MethodNotFoundError, self).__init__(error_code=UNKNOWN_METHOD_ERROR_CODE, message=message)


class NoTargetClusterError(EulerError):
    pass


class RemoteOrNetError(EulerError):
    def __init__(self, **kwargs):
        message = kwargs.pop('message', "remote or network error")
        if kwargs:
            raise TypeError('unexcept arguments: ' + kwargs.keys()[0])
        super(RemoteOrNetError, self).__init__(error_code=REMOTE_OR_NET_ERROR_CODE, message=message)


RemoteOrNetErr = RemoteOrNetError  # For compatible.


class EulerWarning(UserWarning):
    pass


class EulerDeprecatedWarning(EulerWarning):
    pass
