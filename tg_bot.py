from math import ceil

import aiogram
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loguru import logger as log

from _init import assert_all \
    # , _log_call
from _init.__init import _log_call

# Declaring and initializing bot and dispatcher objects
bot: aiogram.Bot = None
storage: MemoryStorage = None
dp: Dispatcher = None


# @_log_call
def secure_str(str, String=str):
    '''
    >>> for i, a in enumerate(filter(bool, map(str.strip, """
    ...     123
    ...     qwertyuiop
    ...     qwertyuiopqwertyuiopqwertyuiop
    ...         """.splitlines()))): print(
    ...     i,
    ...     secure_str(a),
    ...     a,
    ...     sep=' \t'
    ... )
    0       1..3       123
    1       qw..p       qwertyuiop
    2       qwerty..iop       qwertyuiopqwertyuiopqwertyuiop
    '''
    l = len((str := String(str)))
    f, t = ceil(l * .2), ceil(l * .1)
    mf, mt = (2, 1) if l > 5 else (1, 0)
    f, t = max(f, mf), max(t, mt)
    return f"{str[:f]}..{str[-t:]}"


def __init(bot, dp):
    # from ._init import globals as conf
    from _init import globals as conf
    log.info(f"🤖 Init bot!..")
    assert not any((bot, dp)), (bot, dp)

    assert conf.TOKEN, f"TOKEN is empty!"

    # fixme or remove:
    # log.debug(f"# creating bot:"
    #           f">>> {bot.__name__} = {Bot.__name__}(token='{secure_str(conf.TOKEN)}'):..")
    # e:     f">>> {bot.__name__} = {Bot.__name__}(token='{secure_str(conf.TOKEN)}'):..")
    #            ^^^^^^^^^^^^
    # AttributeError: 'NoneType' object has no attribute '__name__'
    bot = Bot(token=conf.TOKEN)
    dp = Dispatcher(bot, storage=storage)
    return bot, dp


@_log_call
def init_bot():
    global bot, dp, storage
    bot, dp = __init(bot, dp)
    storage = MemoryStorage()
    return assert_all(bot, storage, dp)


@_log_call
def init_bot_4_polling():
    global bot, dp
    bot, dp = __init(bot, dp)
    return assert_all(bot, dp)


__all__ = [
    'bot', 'dp'
]


def init_bot_globs():
    from tg_bot import bot, dp
    log.debug(
        f"""# Initialize main globs:
        {bot = }; 
        {dp = }.
        """  # fixme: {storage = };
    )
    # globs = Globals()
    bot = Bot(token=conf.TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
