import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loguru import logger as log

from _init import conf
from _init._init_tools import assert_all
from _init.conf import LOGGING_LEVEL
from _init.env_vars_globs import _log_call, assert_globs
from _init.init_tools import parse_args, load_config, is_env_vars_inited, get_def
from bot.tools import reg_bot_commands
from utils import init_logging, warn


@_log_call
# async
def set_commands(bot: Bot):
    log.info("# Registration of commands displayed in the Telegram interface:..")
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


@_log_call
def main_get_args() -> None:
    log.info(
        f"""# Run main_get_args for getting args from cli: {sys.argv[1:] = }"""
    )
    global globs, dp
    args = parse_args()

    log.info(f"# Load configuration from file <{args.config}>, if specified")
    if not args.config:
        warn(f"Not not args.config!")
    else:
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
    init_logging(
        logging_level=logging.DEBUG if args.debug else LOGGING_LEVEL
    )
    init_env_defaults_by_args(args)
    init_globals_by_args(args)
    init_globs()
    assert_globs()

@_log_call
def init_env_defaults_by_args(args):
    log.info(
        f"""# Initialize environment variables, if not already set by {args = }"""
    )
    os.environ.setdefault("DEBUG", str(args.debug))
    os.environ.setdefault("PORT", str(args.port))
    os.environ.setdefault("TOKEN", str(args.token))
    ##if a.app_name is not None:
    assert args.app_name
    os.environ.setdefault("HEROKU_APP_NAME", str(args.app_name))


@_log_call
def init_globs():
    global bot, storage, dp
    log.debug(
        f"""# Initialize main globs: {bot = }; {storage = }; {dp = }."""
    )
    # globs = Globals()
    bot = Bot(token=conf.TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)


@_log_call
def init_globals_by_args(args):
    log.info("""# Declaring and initializing bot and dispatcher objects""")
    conf.APP_NAME = args.app_name
    conf.TOKEN = args.token
    conf.DEBUG = args.debug
    conf.PORT = args.port
    conf.TIMEOUT = args.timeout


@_log_call
def init_globals():
    log.info("""# Declaring and initializing bot and dispatcher objects""")
    conf.TOKEN = os.getenv('TOKEN')
    conf.DEBUG = os.getenv('DEBUG')
    conf.PORT = os.getenv('PORT')
    conf.TIMEOUT = os.getenv('TIMEOUT')
    conf.APP_NAME = os.getenv('HEROKU_APP_NAME')
    assert_globs()


@_log_call
def init_bot():
    log.info(f"🤖 Init bot!..")
    global bot, storage, dp
    assert conf.TOKEN, f"TOKEN is empty!"

    bot = Bot(token=conf.TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    assert_all(bot, storage, dp)

    return bot, storage, dp
