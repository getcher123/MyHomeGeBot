import logging as logging
import os
from textwrap import shorten
from typing import Any
from warnings import warn

from .calls_logger import log_call
from .logger import *


def get_var(var_name: str, default: Any = None,
            *,
            hangle_fn=log.warning,
            ):
    var_val = os.environ.get(var_name, default)
    if not var_val:
        hangle_fn(f"# not <{var_name}>!")
    return var_val


__all__ = [
    'log',
    'logging',
    'shorten',
    'warn',
]
