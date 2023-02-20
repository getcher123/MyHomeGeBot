import argparse
import builtins
import logging
import os
from typing import Any

from loguru import logger as log

from _init.env_vars_globs import load_param, _log_call

try:
    from PyYAML import yaml
except ImportError as e:
    log.warning(f"? {e}")
    try:
        import yaml
    except ImportError as e:
        log.warning(f"? {e}")



g_env_vars = dict()
print_env_vars_cnt = 0


def print_env_vars():
    global g_env_vars, print_env_vars_cnt
    print_env_vars_cnt += 1
    if not g_env_vars:
        g_env_vars = os.environ.items()
    else:
        ##g_env_vars = os.environ.items() - g_env_vars
        g_env_vars = dict((k, v) for k, v in g_env_vars if k not in dict(g_env_vars).keys())

    builtins.print(f"""#{print_env_vars_cnt} Env vars:
        {g_env_vars}
    """)


class Defaults:
    """Default configuration settings."""
    APP_NAME = '<APP_NAME>'
    YAML_CONFIG_FNAME = 'config.yml'
    DEBUG = True
    PORT = 'WEBAPP_PORT'
    TIMEOUT = 45

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


def parse_args(*, yaml_fname: str = Defaults.YAML_CONFIG_FNAME,
               ):
    """Parse command line arguments."""
    APP_NAME, TOKEN, PORT, DEBUG, TIMEOUT = 'APP_NAME,TOKEN,PORT,DEBUG,TIMEOUT'.split(',')

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, default=yaml_fname,
                        help="Path to YAML configuration file")
    parser.add_argument("--debug", action="store_true", default=get_def(DEBUG),
                        help="Enable debug mode")
    parser.add_argument("--port", type=int, default=get_def(PORT),
                        help="Port number to use for the webhook server")
    parser.add_argument("--token", type=str, default=get_def(TOKEN),
                        help="Telegram Bot API token")
    parser.add_argument("--app_name", type=str, default=get_def(APP_NAME),
                        help="Heroku app name")
    parser.add_argument("--timeout", type=int, default=get_def(TIMEOUT),
                        help="Heroku app name")
    return parser.parse_args()


def assert_file(config_file):
    assert os.path.isfile(config_file), f"No file <{config_file}>!"
    return config_file


@_log_call
def load_config(config_file):
    """Load configuration from a YAML file."""
    assert_file(config_file)
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    return config


@_log_call
def save_defaults_to_yaml(file_path):
    """Save default configuration settings to a YAML file."""
    defaults = {
        "debug": Defaults.DEBUG,
        "port": Defaults.PORT,
        "token": Defaults.TOKEN,
        "app_name": Defaults.APP_NAME,
        "TIMEOUT": 30,
    }
    with open(file_path, "w") as f:
        yaml.dump(defaults, f, default_flow_style=False)


@_log_call
def set_env_var(env_var_name: str, val: Any = None):
    os.environ[env_var_name] = (value := val or env_var_name)
    logging.debug(f"# Env var <{env_var_name}> set to <{value}>")


@_log_call
def is_env_vars_inited():
    return bool(os.getenv('TOKEN', ''))
