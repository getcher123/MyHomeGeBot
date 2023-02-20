import os
from typing import Any

from loguru import logger as log

from settings.conf import CONF


@log.catch
def check_globs(name, val, *, exit_if_not_set=CONF.EXIT_IF_ENV_VAR_NOT_SET):
    # Checking for the existence of a variable
    if not val:
        msg = f"not {name}!"
        log.error(msg)
        if exit_if_not_set:
            exit()
        else:
            raise Exception(msg)


@log.catch
# @log_call
def set_glob(name: str, val: Any):
    globals()[name] = val = os.getenv(name)
    check_globs(name, val)
    return val
