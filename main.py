# With code below do next:
# - add initialazing next env var by argparse or yaml with defaults: DEBUG,PORT,TOKEN,HEROKU_APP_NAME
# - place defauls in some separate class
# - add generation of yaml func with defaults

"""Webwook entry point"""
import asyncio
import os
import utils

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook

from bot.handlers import common
from plugins import check_new_houses
from bot.bot_commands_settings import commands
from settings.bot_settings import TOKEN
from settings.conf import CONF
from settings.webhook_settings import (WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT)
from utils import logging
from utils.logger import init_logging
from utils.telegrammy import TelegramBot

commands = commands
# logger = logging.getLogger(__name__)
logger = utils.getLogger(__name__)

# Declaring and initializing bot and dispatcher objects
bot = Bot(token=TOKEN)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

# Registration of commands displayed in the Telegram interface
async def set_commands(bot: Bot):
    logging.debug(f'#3 {commands = }')
    global commands
    commands = reg_bot_commands(
        start="Bot start🚀",
        help="Help🆘",
        set_link='установить новую ссылку для поиска',
        show='посмотреть всю выдачу',
        cancel='отменить действие',
        show_link='Посмотреть текущую ссылку для поиска',
    )
    logging.debug(f'#4 {commands = }')


async def on_startup(dispatcher) -> None:
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    await bot.set_my_commands(commands)

    loop = asyncio.get_event_loop()
    loop.create_task(check_new_houses(dp, int(os.getenv('TIMEOUT'))))


async def on_shutdown(dispatcher) -> None:
    await bot.delete_webhook()


def main() -> None:
    init_logging()

    # Registration of handlers
    common.register_client_handlers(dp)
    # Installing bot commands
    set_commands(bot)

    # Webhook start
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )


if CONF.INIT_TelegramBot:
    telegramBot = TelegramBot(TOKEN)


def main_get_args():
    pass


if __name__ == '__main__':
    if os.getenv('TOKEN', ''):
        main()
    else:
        main_get_args()
