"""Webwook entry point
    # With code below do next:
    # - add initialazing next env var by argparse or yaml with defaults: val,PORT,TOKEN,HEROKU_APP_NAME
    # - place defauls in some separate class
    # - add generation of yaml func with defaults
"""

from aiogram.utils.executor import start_webhook

import _init.asserts
import tg_bot
from _init import init_globals_by_env_vars, assert_globs, parse_args
from _init.after_init import set_commands
# from _init.env_vars_globs import is_it_on_heroku_running
from _init.asserts import get_env_vars_dict
from _init.env_vars_globs import is_it_on_heroku_running
from bot.handlers import common
from settings import CONF
from settings.webhook_settings import (WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT)
from tg_bot import init_bot
from utils import init_logging, getLogger, log

logger = getLogger(__name__)


def is_evn_vars_set():
    return all(get_env_vars_dict().values())
    ##?r return os.getenv('TOKEN')


@log.catch
def main_regular() -> None:
    import utils

    if not is_evn_vars_set():
        utils.warn(f"not is_evn_vars_set():..")

    if is_it_on_heroku_running():
        _init.env_vars.env_setdefaults_by_args(
            args=parse_args()
        )
    init_globals_by_env_vars()
    assert_globs()

    init_logging()

    tg_bot.bot, tg_bot.storage, tg_bot.dp = init_bot()

    log.debug(f"# Registration of handlers:..")
    common.register_client_handlers(tg_bot.dp)

    set_commands(tg_bot.bot)

    from _init.after_init import on_startup, on_shutdown

    log.debug(f"# Webhook start:..")
    start_webhook(
        dispatcher=tg_bot.dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
    log.debug(f"✅")


def main():
    from _init.initools import is_it_on_heroku_running
    assert is_it_on_heroku_running()

    if is_it_on_heroku_running():
        main_regular()
    else:
        from _init.init_main import init_local_run
        init_local_run()


if __name__ == '__main__':
    if CONF.ALWAYS_RUN_DOCTESTS:
        from doctest import testmod

        testmod()

    main()

# fixme 1st!
# 2023-02-20T03:04:32.287218+00:00 app[web.1]:   File "/app/plugins/home_parser/messages/sender.py", line 42, in send_messages
#
# 2023-02-20T03:04:32.287218+00:00 app[web.1]:     await send_photo(
#
# 2023-02-20T03:04:32.287219+00:00 app[web.1]:   File "/app/utils/telegrammy/__init__.py", line 16, in send_photo
#
# 2023-02-20T03:04:32.287219+00:00 app[web.1]:     await telegramBot.send_photo_handled(
#
# 2023-02-20T03:04:32.287219+00:00 app[web.1]: TypeError: 'coroutine' object is not callable
