import os
import sys

from loguru import logger as log

from _init import (
    # _log_call,
    assert_globs, is_env_vars_inited,
    parse_args, load_config, env_setdefaults_by_args,
    init_globals_by_env_vars, get_globs,
    globals as conf)
from _init.__init import _log_call
from settings import CONF
from tg_bot import init_bot_globs
from utils import logging


@_log_call
def init_local_run(*, dbg=CONF.IS_DEBUG):
    # from _init.env_vars_globs import is_it_on_heroku_running
    if not is_env_vars_inited():
        # fixme!
        # from _init.initools import is_it_on_heroku_running
        # assert not is_it_on_heroku_running()
        main_get_args()
        assert_globs()
    else:
        logging.info(f"All args're ok: ")
    if dbg:
        return {
            a: os.getenv(a) for a in conf.__dir__()
            if a.replace('_', '').isupper()
        }


@log.catch
@_log_call
def main_get_args() -> None:
    from utils import init_logging, warn

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
        args.USER_IDS = config.get("USER_IDS", args.USER_IDS)

        log.debug(f"""###
        {args.debug =}   
        {args.port =  }  
        {args.token =  } 
        {args.app_name =}
        """)

    from _init.globals import LOGGING_LEVEL
    init_logging(
        logging_level=logging.DEBUG if args.debug else LOGGING_LEVEL
    )
    from _init import assert_all
    log.debug(f"""
        {assert_all(
        env_setdefaults_by_args(args)
                    ) = }
    """)
    assert_globs()

    ##?c init_globals_by_args(args)
    init_globals_by_env_vars()
    init_bot_globs()
    print(f"""
    {get_globs() = }
    """)
    assert_globs()
