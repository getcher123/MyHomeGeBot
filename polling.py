"""Polling entry point"""
import asyncio

from aiogram import Bot
# !w fixme from utils import log
from loguru import logger as log

from _init.env_vars_globs import (
    is_it_on_heroku_running, assert_globs, get_globs)
from _init.init_main import init_local_run


# # Declaring and initializing bot and dispatcher objects
# bot = Bot(token=TOKEN)
# dp = Dispatcher(bot)


async def set_commands(bot: Bot):
    from bot.bot_commands_settings import commands

    log.info("# Registration of commands displayed in the Telegram interface")
    await bot.set_my_commands(commands)


@log.catch
async def polling_main_regular() -> None:
    init_local_run()

    from utils import logging, init_logging, log
    logger = logging.getLogger(__name__)

    from tg_bot import init_bot_4_polling
    from bot.handlers import common

    log.info('# Setting up logging')
    init_logging()

    bot, dp = init_bot_4_polling()

    log.info('# Registration of handlers')
    common.register_client_handlers(dp)

    log.info('# Installing bot commands')
    await set_commands(bot)

    log.info('# Polling start')
    await dp.start_polling()


async def main():
    from _init.init_main import init_local_run
    assert not is_it_on_heroku_running()

    init_local_run()
    print(f"""
    {get_globs() = }
    """)
    assert_globs()

    await polling_main_regular()


if __name__ == '__main__':
    asyncio.run(main())
