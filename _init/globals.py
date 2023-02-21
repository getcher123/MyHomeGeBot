import logging
import os

from loguru import logger as log

from . import Defaults as conf

# from .__init import _log_call
# from .asserts import assert_env_vars, assert_globs

TOKEN: str = None
HEROKU_APP_NAME: str = None
DEBUG: str = 'None'
PORT: int = None
TIMEOUT: int = None
LOGGING_LEVEL: int = 10
USER_IDS: str = '???,xxx'


# class Globals:
#     def __init__(self,
#                  ):
#         from _init import is_env_vars_inited
#         from Defaults import get_def
#
#         assert is_env_vars_inited()
#         self.TIMEOUT = int(os.getenv('TIMEOUT', get_def('TIMEOUT')))


# @_log_call(with_call_stack=True)
def init_debug():
    from settings import check_globs
    global DEBUG, LOGGING_LEVEL
    # ~? DEBUG = set_glob('DEBUG')

    # # Getting the DEBUG value from an environment variable
    DEBUG = os.getenv('DEBUG', DEBUG)
    check_globs('DEBUG', DEBUG)

    if DEBUG:
        LOGGING_LEVEL = logging.DEBUG
    else:
        LOGGING_LEVEL = logging.INFO


def init_globals_by_args(args):
    log.info(f"""> init_globals_by_args({args = })""")
    conf.HEROKU_APP_NAME = args.app_name
    conf.TOKEN = args.token
    conf.DEBUG = args.debug
    conf.PORT = args.port
    conf.TIMEOUT = args.timeout


# @_log_call
def init_globals_by_env_vars():
    log.info("""> init_globals_by_env_vars:..""")
    from _init import assert_env_vars, assert_globs
    assert_env_vars()

    conf.TOKEN = os.getenv('TOKEN')
    conf.DEBUG = os.getenv('DEBUG')
    conf.PORT = int(os.getenv('PORT'))
    conf.TIMEOUT = int(os.getenv('TIMEOUT'))
    conf.HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
    assert_globs()
