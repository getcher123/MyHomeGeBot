import socket

from loguru import logger as log

from settings import CONF

try:
    from PyYAML import yaml
except ImportError as e:
    log.warning(f"? {e}")
    try:
        import yaml
    except ImportError as e:
        log.warning(f"? {e}")
_logd = print


# @_log_call
def is_it_on_heroku_running():
    log.debug(f"# {(hostname := socket.gethostname()) = }")
    return (not hostname.endswith(CONF.LAPTOP_LOCALHOST_NAME)
            or CONF.IGNORE_LOCAL_START_HEROKU_CONF
            )
