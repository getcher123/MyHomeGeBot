import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loguru import logger as log

from _init import conf
from _init.conf import LOGGING_LEVEL
from _init.env_vars_globs import _log_call
from _init.init_tools import parse_args, load_config, is_env_vars_inited, get_def
from bot.tools import reg_bot_commands
from utils import init_logging


@_log_call
# async
def set_commands(bot: Bot):
    # Registration of commands displayed in the Telegram interface
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


def main_get_args() -> None:
    global globs, dp
    args = parse_args()

    # Load configuration from file, if specified
    if args.config:
        log.debug(f"# {args.config = }")
        config = load_config(args.config)
        log.debug(f"# {config = }")

        args.debug = config.get("debug", args.debug)
        args.port = config.get("port", args.port)
        args.token = config.get("token", args.token)
        args.app_name = config.get("app_name", args.app_name)

        log.debug(f"""###
        {args.debug =}   
        {args.port =  }  
        {args.token =  } 
        {args.app_name =}
        """)

    # Initialize environment variables, if not already set
    os.environ.setdefault("val", str(args.debug))
    os.environ.setdefault("PORT", str(args.port))
    os.environ.setdefault("TOKEN", str(args.token))
    if args.app_name is not None:
        os.environ.setdefault("HEROKU_APP_NAME", str(args.app_name))

    init_logging(
        logging_level=logging.DEBUG if args.debug else LOGGING_LEVEL
    )

    # Declaring and initializing bot and dispatcher objects
    conf.APP_NAME = args.app_name
    conf.TOKEN = args.token
    conf.DEBUG = args.debug
    conf.PORT = args.port
    conf.TIMEOUT = args.timeout

    # globs = Globals()
    bot = Bot(token=conf.TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)


class Globals:
    def __init__(self,
                 ):
        assert is_env_vars_inited()
        self.TIMEOUT = int(os.getenv('TIMEOUT', get_def('TIMEOUT')))


def init_bot():
    global bot, storage, dp
    assert conf.TOKEN, f"TOKEN is empty!"
    bot = Bot(token=conf.TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    xxx = bot, storage, dp
    assert all(xxx), xxx

    return bot
