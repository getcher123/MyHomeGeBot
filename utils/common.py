import asyncio
import os
from textwrap import shorten
from typing import Any

# import logging as log
from .logger import log


def shorten(a: Any, len: int, shorten=shorten):
    return shorten(str(a), len)


async def sleep(sleep_time: int, descr: str = ''):
    log.debug(f"Sleep for {sleep_time}..{f' ({descr})' if descr else ''}")
    await asyncio.sleep(sleep_time)


def get_var(var_name: str, default: Any = None,
            *,
            hangle_fn=log.warning,
            ):
    var_val = os.environ.get(var_name, default)
    if not var_val:
        hangle_fn(f"# not <{var_name}>!")
    return var_val
