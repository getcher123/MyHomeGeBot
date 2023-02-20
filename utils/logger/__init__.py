# todo: consolidate loggers!
import logging as log
import logging as logging

from loguru import logger

from _init.conf import LOGGING_LEVEL
from _init.env_vars_globs import _log_call
from settings.debug_settings import init_debug
from utils.logger.calls_logger import get_a_kw_call_str

getLogger = logging.getLogger


@_log_call
def init_logging(*,
                 logging_level=LOGGING_LEVEL
                 ):
    log.info(f"💻 Init logging:..")

    # ? from settings.debug_settings import LOGGING_LEVEL
    init_debug()
    # Setting up logging
    logging.basicConfig(
        level=logging_level,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    return logging


log, logging, logger
