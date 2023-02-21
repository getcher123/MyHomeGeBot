from loguru import logger as log

from _init.asserts import assert_file
from _init.yamly import load_param

try:
    from PyYAML import yaml
except ImportError as e:
    log.warning(f"? {e}")
    try:
        import yaml
    except ImportError as e:
        log.warning(f"? {e}")


class Defaults:
    """Default configuration settings."""
    HEROKU_APP_NAME = '<HEROKU_APP_NAME>'
    YAML_CONFIG_FNAME = 'config.yml'
    DEBUG = True
    PORT = 'WEBAPP_PORT'
    TIMEOUT = 45

    # USER_IDS =

    def get(self, name):
        """
        >>> Defaults().get('TEST123')
        True
        >>> Defaults().get('TEST123')
        Traceback (most recent call last):
        ...
        Exception: No attr <TEST123> for Defaults
        """
        if name in Defaults.__dict__.keys():
            return self.__getattribute__(name)
        else:
            raise Exception(f"No attr <{name}> for {Defaults.__name__}")


def get_def(name, *, yaml_fname: str = Defaults.YAML_CONFIG_FNAME):
    assert_file(yaml_fname)
    return load_param(yaml_fname, name) or Defaults().get(name)
