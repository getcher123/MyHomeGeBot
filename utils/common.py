import asyncio
import os
from textwrap import shorten
from typing import Any

# import logging as log
from .logs import log


def shorten(a: Any, len: int, shorten=shorten):
    return shorten(str(a), len)


async def sleep(sleep_time: int, descr: str = ''):
    try:
        log.info(f"Sleep for {sleep_time}..{f' ({descr})' if descr else ''}")
        await asyncio.sleep(sleep_time)
    except:
        log.exception(f"# fixme: {sleep_time=}")
        await asyncio.sleep(30)


def get_var(var_name: str, default: Any = None,
            *,
            hangle_fn=log.warning,
            ):
    var_val = os.environ.get(var_name, default)
    if not var_val:
        hangle_fn(f"# not <{var_name}>!")
    return var_val
