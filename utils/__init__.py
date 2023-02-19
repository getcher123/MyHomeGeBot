from warnings import warn

from utils.logger.calls_logger import log_call
from .common import *
##from textwrap import shorten
from .common import shorten
from .logger import log, logging, init_logging, logger, getLogger

__all__ = [
    'log',
    'logger',
    'logging',
    'shorten',
    'warn',
    'sleep',
    'get_var',
]
