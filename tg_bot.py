import aiogram
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loguru import logger as log

from _init import conf, assert_all, _log_call

# Declaring and initializing bot and dispatcher objects
bot: aiogram.Bot = None
storage: MemoryStorage = None
dp: Dispatcher = None


# @_log_call
def init_bot():
    log.info(f"🤖 Init bot!..")
    global bot, storage, dp
    assert conf.TOKEN, f"TOKEN is empty!"

    bot = Bot(token=conf.TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    assert_all(bot, storage, dp)

    return bot, storage, dp


@_log_call
def init_bot1():
    log.info(f"🤖 Init bot!..")
    global bot, dp
    assert conf.TOKEN, f"TOKEN is empty!"

    bot = Bot(token=conf.TOKEN)
    dp = Dispatcher(bot, storage=storage)

    assert_all(bot, dp)

    return bot, dp


__all__ = [
    'bot', 'dp'
]
