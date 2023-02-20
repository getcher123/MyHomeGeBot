# d from _log_call import _logd;_logd(__file__)
from warnings import warn

from .common import *
from .common import shorten
from .logs import log, logging, init_logging, logger, getLogger
from .logs.calls_logger import log_call

# print = log.info
print = logger.info

__all__ = [
    'log',
    'logger',
    'logging',
    'shorten',
    'warn',
    'sleep',
    'get_var',
]
