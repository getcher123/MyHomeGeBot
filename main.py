"""Webwook entry point
    # With code below do next:
    # - add initialazing next env var by argparse or yaml with defaults: val,PORT,TOKEN,HEROKU_APP_NAME
    # - place defauls in some separate class
    # - add generation of yaml func with defaults
"""

from aiogram.utils.executor import start_webhook

import tg_bot
from _init import set_commands, main_get_args, init_globals, assert_globs
from _init.env_vars_globs import is_it_on_heroku_running
from _init.init_tools import is_env_vars_inited
from bot.handlers import common
from settings import CONF
from settings.webhook_settings import (WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT)
from tg_bot import init_bot
from utils import init_logging, getLogger, log

logger = getLogger(__name__)

def main_regular() -> None:
    init_globals()
    assert_globs()

    init_logging()

    tg_bot.bot, tg_bot.storage, tg_bot.dp = init_bot()

    log.debug(f"# Registration of handlers:..")
    common.register_client_handlers(tg_bot.dp)

    set_commands(tg_bot.bot)

    from _init.after_init import on_startup, on_shutdown

    log.debug(f"# Webhook start:..")
    start_webhook(
        dispatcher=tg_bot.dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
    log.debug(f"✅")


def main():
    if is_it_on_heroku_running():
        main_regular()
    else:
        if not is_env_vars_inited():
            assert not is_it_on_heroku_running()
            main_get_args()
            assert_globs()


if __name__ == '__main__':
    if CONF.ALWAYS_RUN_DOCTESTS:
        from doctest import testmod

        testmod()

    main()
