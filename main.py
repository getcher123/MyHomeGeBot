# With code below do next:
# - add initialazing next env var by argparse or yaml with defaults: val,PORT,TOKEN,HEROKU_APP_NAME
# - place defauls in some separate class
# - add generation of yaml func with defaults
"""Webwook entry point"""

import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook

from _init import set_commands, main_get_args, init_bot
from _init.init_tools import print_env_vars, set_env_var, is_env_vars_inited
from bot.handlers import common
from settings import CONF
from settings.webhook_settings import (WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT)
from utils import init_logging, getLogger, log

# from init import set_commands
# from settings.bot_settings import init_settings_token

logger = getLogger(__name__)
print = log.info

# Declaring and initializing bot and dispatcher objects
bot: aiogram.Bot = None
storage: MemoryStorage = None
dp: Dispatcher = None


def main_regular() -> None:
    init_logging()

    bot = init_bot()
    assert bot

    log.debug(f"# Registration of handlers")
    common.register_client_handlers(dp)

    set_commands(bot)

    from _init.after_init import on_startup, on_shutdown
    assert bot

    log.debug(f"# Webhook start")
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )


def main():
    set_env_var('HEROKU_APP_NAME')
    if not is_env_vars_inited():
        print_env_vars()
        main_get_args()
        print_env_vars()
    main_regular()


if __name__ == '__main__':
    if CONF.ALWAYS_RUN_DOCTESTS:
        from doctest import testmod

        testmod()

    main()
