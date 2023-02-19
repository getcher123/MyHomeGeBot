"""Settings required for logging in DEBUG mode"""
# !w from utils \
import logging
import os

from settings import check_globs

# Getting the DEBUG value from an environment variable
DEBUG = os.getenv('DEBUG')
check_globs('DEBUG', DEBUG)

if DEBUG:
    LOGGING_LEVEL = logging.DEBUG
else:
    LOGGING_LEVEL = logging.INFO
