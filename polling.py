"""Polling entry point"""
import asyncio

from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from _init.conf import TOKEN
from bot.bot_commands_settings import commands
from bot.handlers import common
from utils import logging, init_logging, log

##?c from settings.bot_settings import TOKEN

logger = logging.getLogger(__name__)

# Declaring and initializing bot and dispatcher objects
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


async def set_commands(bot: Bot):
    # Registration of commands displayed in the Telegram interface
    await bot.set_my_commands(commands)


async def main() -> None:
    log.debug('# Setting up logging')
    init_logging()

    log.debug('# Registration of handlers')
    common.register_client_handlers(dp)

    log.debug('# Installing bot commands')
    await set_commands(bot)

    log.debug('# Polling start')
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())