import asyncio
# import logging as log
from . import log

async def sleep(sleep_time: int, desc: str = ''):
    log.debug(f"Sleep for {sleep_time}..{f' ({descr})' if descr else ''}")
    await asyncio.sleep(sleep_time)
