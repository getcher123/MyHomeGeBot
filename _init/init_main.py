import os

from _init import _log_call, conf
from settings import CONF
from utils import logging


@_log_call
def init_local_run(*, dbg=CONF.IS_DEBUG):
    from _init import is_env_vars_inited, main_get_args, assert_globs
    from _init.env_vars_globs import is_it_on_heroku_running
    if not is_env_vars_inited():
        assert not is_it_on_heroku_running()
        main_get_args()
        assert_globs()
    else:
        logging.info(f"All args're ok: ")
    if dbg:
        return {
            a: os.getenv(a) for a in conf.__dir__()
            if a.replace('_', '').isupper()
        }
