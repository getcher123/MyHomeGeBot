"""Polling entry point"""
import asyncio

from aiogram import Bot

from _init import _log_call


# # Declaring and initializing bot and dispatcher objects
# bot = Bot(token=TOKEN)
# dp = Dispatcher(bot)


async def set_commands(bot: Bot):
    from bot.bot_commands_settings import commands

    # Registration of commands displayed in the Telegram interface
    await bot.set_my_commands(commands)


@_log_call
def init_local_run():
    from _init import is_env_vars_inited
    if not is_env_vars_inited():
        from _init.env_vars_globs import is_it_on_heroku_running
        assert not is_it_on_heroku_running()
        from _init import main_get_args
        main_get_args()
        from _init import assert_globs
        assert_globs()


async def main() -> None:
    init_local_run()

    from utils import logging, init_logging, log
    logger = logging.getLogger(__name__)

    from tg_bot import init_bot1
    from bot.handlers import common

    log.info('# Setting up logging')
    init_logging()

    bot, dp = init_bot1()

    log.debug('# Registration of handlers')
    common.register_client_handlers(dp)

    log.debug('# Installing bot commands')
    await set_commands(bot)

    log.debug('# Polling start')
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())