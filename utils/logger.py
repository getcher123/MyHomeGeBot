import logging
import logging as log
import logging as logging
from loguru import logger
#todo: consolidate loggers!
from settings.debug_settings import LOGGING_LEVEL

log.basicConfig(level=LOGGING_LEVEL)

log, logging, logger


def init_logging():
    # Setting up logging
    logging.basicConfig(
        level=LOGGING_LEVEL,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    return logging
