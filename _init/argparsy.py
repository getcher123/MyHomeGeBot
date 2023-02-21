import argparse

from .Defaults import Defaults

csv = str


def parse_args(*, yaml_fname: str = Defaults.YAML_CONFIG_FNAME,
               ):
    """Parse command line arguments."""
    from .Defaults import get_def

    HEROKU_APP_NAME, TOKEN, PORT, DEBUG, TIMEOUT, USER_IDS = 'HEROKU_APP_NAME,TOKEN,PORT,DEBUG,TIMEOUT,USER_IDS'.split(
        ',')

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, default=yaml_fname,
                        help="Path to YAML configuration file")
    parser.add_argument("--debug", action="store_true", default=get_def(DEBUG),
                        help="Enable debug mode")
    parser.add_argument("--port", type=int, default=get_def(PORT),
                        help="Port number to use for the webhook server")
    parser.add_argument("--token", type=str, default=get_def(TOKEN),
                        help="Telegram Bot API token")
    parser.add_argument("--app_name", type=str, default=get_def(HEROKU_APP_NAME),
                        help="Heroku app name")
    parser.add_argument("--timeout", type=int, default=get_def(TIMEOUT),
                        help="Heroku app name")
    parser.add_argument("--USER_IDS", type=csv, default=get_def(USER_IDS),
                        help="<USER_IDS>")

    return parser.parse_args()
