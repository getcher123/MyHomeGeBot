import logging
import os

from _init.env_vars_globs import _log_call
from settings import check_globs

TOKEN: str = None
APP_NAME: str = None
DEBUG: str = None
PORT: int = None
TIMEOUT: int = None
LOGGING_LEVEL: int = 10


@_log_call(with_call_stack=True)
def init_debug():
    global DEBUG, LOGGING_LEVEL
    # ~? DEBUG = set_glob('DEBUG')

    # # Getting the DEBUG value from an environment variable
    DEBUG = os.getenv('DEBUG')
    check_globs('DEBUG', DEBUG)

    if DEBUG:
        LOGGING_LEVEL = logging.DEBUG
    else:
        LOGGING_LEVEL = logging.INFO
