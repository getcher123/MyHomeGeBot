import logging as log
from textwrap import shorten

from settings.debug_settings import LOGGING_LEVEL

log.basicConfig(level=LOGGING_LEVEL)
π
__all__ = [
    'log',
    'shorten',
]
