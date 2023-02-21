import logging
import os

from settings import check_globs

TOKEN: str = None
HEROKU_APP_NAME: str = None
DEBUG: str = 'None'
PORT: int = None
TIMEOUT: int = None
LOGGING_LEVEL: int = 10
USER_IDS: str = '???,xxx'

class Globals:
    def __init__(self,
                 ):
        from _init import is_env_vars_inited
        from _init import get_def

        assert is_env_vars_inited()
        self.TIMEOUT = int(os.getenv('TIMEOUT', get_def('TIMEOUT')))


# @_log_call(with_call_stack=True)
def init_debug():
    global DEBUG, LOGGING_LEVEL
    # ~? DEBUG = set_glob('DEBUG')

    # # Getting the DEBUG value from an environment variable
    DEBUG = os.getenv('DEBUG', DEBUG)
    check_globs('DEBUG', DEBUG)

    if DEBUG:
        LOGGING_LEVEL = logging.DEBUG
    else:
        LOGGING_LEVEL = logging.INFO
