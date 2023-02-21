# todo: consolidate loggers!
##import logging as log
import logging as logging

from loguru import logger
from loguru import logger as log

# from _init.conf import init_debug
from settings.debug_settings import LOGGING_LEVEL
from utils.logs.calls_logger import get_a_kw_call_str
from ..common import warn

# from _init.conf import LOGGING_LEVEL

getLogger = logging.getLogger
g_logging_level = None if not 'logging_level' in globals().keys() else globals()['g_logging_level']


# from _init import _log_call
# @_log_call
def init_logging(*,
                 logging_level=LOGGING_LEVEL
                 ):
    # from settings.debug_settings import init_debug

    log.info(f"💻 Init logging:.. {logging_level = }")

    global g_logging_level
    if g_logging_level:
        warn(f"{g_logging_level = } was already set! Now'll be -> {logging_level = }...")

    # ? from settings.debug_settings import LOGGING_LEVEL
    from _init.globals import init_debug
    init_debug()
    # Setting up logging
    logging.basicConfig(
        level=logging_level,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    return log, logging, logger
