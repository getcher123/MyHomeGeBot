"""Webwook entry point
    # With code below do next:
    # - add initialazing next env var by argparse or yaml with defaults: val,PORT,TOKEN,HEROKU_APP_NAME
    # - place defauls in some separate class
    # - add generation of yaml func with defaults
"""

import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook

from _init import set_commands, main_get_args, init_bot, _log_call, init_globals, assert_globs
from _init.env_vars_globs import is_it_on_heroku_running
from _init.init_tools import is_env_vars_inited
from bot.handlers import common
from settings import CONF
from settings.webhook_settings import (WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT)
from utils import init_logging, getLogger, log

logger = getLogger(__name__)
# print = log.info
print = logger.info

# Declaring and initializing bot and dispatcher objects
bot: aiogram.Bot = None
storage: MemoryStorage = None
dp: Dispatcher = None


@_log_call
def main_regular() -> None:
    global bot, storage, dp
    init_globals()
    assert_globs()

    init_logging()

    bot, storage, dp = init_bot()

    log.debug(f"# Registration of handlers:..")
    common.register_client_handlers(dp)

    set_commands(bot)

    from _init.after_init import on_startup, on_shutdown

    log.debug(f"# Webhook start:..")
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
    log.debug(f"✅")


@_log_call
def main():
    if is_it_on_heroku_running():
        main_regular()
    else:
        # set_env_var('HEROKU_APP_NAME')
        if not is_env_vars_inited():
            assert not is_it_on_heroku_running()
            # print_env_vars()
            main_get_args()
            # print_env_vars()
            assert_globs()


if __name__ == '__main__':
    if CONF.ALWAYS_RUN_DOCTESTS:
        from doctest import testmod

        testmod()

    main()
