"""Polling entry point"""
import asyncio
import os

from aiogram import Bot
# !w fixme from utils import log
from loguru import logger as log

import _init
# from _init.env_vars_globs import (
#     is_it_on_heroku_running)
from _init import assert_globs, init_globals_by_env_vars
from tg_bot import bot, dp


# # Declaring and initializing bot and dispatcher objects
# bot = Bot(token=TOKEN)
# dp = Dispatcher(bot)


async def set_commands(bot: Bot):
    from bot.bot_commands_settings import commands

    log.info("# Registration of commands displayed in the Telegram interface")
    await bot.set_my_commands(commands)


@log.catch
async def polling_main_regular() -> None:
    log.info('# Installing bot commands')
    await set_commands(bot)

    await dp.start_polling()


# async def main(): await polling_main_regular()


def main():
    from _init.init_main import init_local_run
    # fixme!
    # assert not (is_it_on_heroku_running()
    #             or CONF.IGNORE_LOCAL_START_HEROKU_CONF
    #             )

    init_local_run()

    from utils import logging, init_logging, log
    logger = logging.getLogger(__name__)

    from tg_bot import init_bot_4_polling
    from bot.handlers import common

    log.info('# Setting up logging')
    init_logging()

    assert_globs()

    from _init import parse_args
    _init.env_vars.env_setdefaults_by_args(
        parse_args()
    )

    init_globals_by_env_vars()
    assert_globs()

    log.warning(f"""###>
        {_init.asserts.assert_env_vars() = }
    """)
    log.warning(f"""###>
        {_init.asserts.assert_globs() = }
    """)

    bot, dp = init_bot_4_polling()

    log.info('# Registration of handlers')
    common.register_client_handlers(dp)

    log.info('# Polling start')
    log.warning(f">>> {os.getenv('TOKEN') = }")

    ##? asyncio.run(main())
    asyncio.run(polling_main_regular())


if __name__ == '__main__':
    main()
