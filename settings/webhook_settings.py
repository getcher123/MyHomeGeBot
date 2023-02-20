"""Settings required to run the webhook"""
import os

from loguru import logger as log

from _init.conf import TOKEN
from _init.env_vars_globs import _log_call
from . import CONF

# Application name
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# Webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# Webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)


@log.catch
@_log_call(with_call_stack=True)
def __set_local_env_vars(*, raise_exc=CONF.RAISE_IF_ENV_VAR_NOT_SET):
    # Сhecking for the existence of a variable
    if (
            not HEROKU_APP_NAME
            or not WEBAPP_PORT
    ):
        log.error(msg := f"""
            not {HEROKU_APP_NAME = }
            or not {WEBAPP_PORT = }
        """)
        if raise_exc:
            raise Exception(msg)
        else:
            exit()
