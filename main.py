# With code below do next:
# - add initialazing next env var by argparse or yaml with defaults: DEBUG,PORT,TOKEN,HEROKU_APP_NAME
# - place defauls in some separate class
# - add generation of yaml func with defaults

"""Webwook entry point"""
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

import utils
from bot.handlers import common
from settings.bot_settings import TOKEN
from settings.conf import CONF
from utils.logger import init_logging
from utils.telegrammy import TelegramBot
from utils.telegrammy.tools import reg_bot_commands

# logger = logging.getLogger(__name__)
logger = utils.getLogger(__name__)

# Declaring and initializing bot and dispatcher objects
bot = Bot(token=TOKEN)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

import argparse
import asyncio
import os
import yaml

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers import common
from plugins import check_new_houses
from settings.bot_commands_settings import commands
from settings.bot_settings import TOKEN
from settings.debug_settings import LOGGING_LEVEL, check_globs
from settings.webhook_settings import (WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT)

from utils import logging

logger = logging.getLogger(__name__)


class Defaults:
    """Default configuration settings."""
    DEBUG = False
    PORT = WEBAPP_PORT
    TOKEN = TOKEN
    APP_NAME = None


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, default=None,
                        help="Path to YAML configuration file")
    parser.add_argument("--debug", action="store_true", default=False,
                        help="Enable debug mode")
    parser.add_argument("--port", type=int, default=Defaults.PORT,
                        help="Port number to use for the webhook server")
    parser.add_argument("--token", type=str, default=Defaults.TOKEN,
                        help="Telegram Bot API token")
    parser.add_argument("--app-name", type=str, default=Defaults.APP_NAME,
                        help="Heroku app name")
    return parser.parse_args()


def load_config(config_file):
    """Load configuration from a YAML file."""
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    return config


def save_defaults_to_yaml(file_path):
    """Save default configuration settings to a YAML file."""
    defaults = {
        "debug": Defaults.DEBUG,
        "port": Defaults.PORT,
        "token": Defaults.TOKEN,
        "app_name": Defaults.APP_NAME,
    }
    with open(file_path, "w") as f:
        yaml.dump(defaults, f, default_flow_style=False)


def main_get_args() -> None:
    args = parse_args()

    # Load configuration from file, if specified
    if args.config:
        config = load_config(args.config)
        args.debug = config.get("debug", args.debug)
        args.port = config.get("port", args.port)
        args.token = config.get("token", args.token)
        args.app_name = config.get("app_name", args.app_name)

    # Initialize environment variables, if not already set
    os.environ.setdefault("DEBUG", str(args.debug))
    os.environ.setdefault("PORT", str(args.port))
    os.environ.setdefault("TOKEN", str(args.token))
    if args.app_name is not None:
        os.environ.setdefault("HEROKU_APP_NAME", str(args.app_name))

    # Setting up logging
    logging_level = logging.DEBUG if args.debug else LOGGING_LEVEL
    logging.basicConfig(
        level=logging_level,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Declaring and initializing bot and dispatcher objects
    bot = Bot(token=args.token)

    storage = MemoryStorage()

    dp = Dispatcher(bot, storage=storage)

    # Registration of commands displayed in the Telegram interface
    async def set_commands(bot: Bot):
        logging.debug(f'{commands = }')

    async def on_startup(dispatcher) -> None:
        await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


# Registration of commands displayed in the Telegram interface
async def set_commands(bot: Bot):
    # global commands
    from bot.bot_commands_settings import commands

    logging.debug(f'#3 {commands = }')
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

    check_globs()

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




if __name__ == '__main__':
    if os.getenv('TOKEN', ''):
        main()
    else:
        main_get_args()
