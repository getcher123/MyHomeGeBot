import logging
import os
from argparse import Namespace
from typing import Any

from loguru import logger as log

# from _init import _log_call
from _init.asserts import all_

g_env_vars = dict()
print_env_vars_cnt = 0


def print_env_vars():
    global g_env_vars, print_env_vars_cnt
    print_env_vars_cnt += 1
    if not g_env_vars:
        g_env_vars = os.environ.items()
    else:
        ##g_env_vars = os.environ.items() - g_env_vars
        g_env_vars = dict((k, v) for k, v in g_env_vars if k not in dict(g_env_vars).keys())

    builtins.print(f"""#{print_env_vars_cnt} Env vars:
        {g_env_vars}
    """)


def set_env_var(env_var_name: str, val: Any = None):
    os.environ[env_var_name] = (value := val or env_var_name)
    logging.debug(f"# Env var <{env_var_name}> set to <{value}>")


# @_log_call
def is_env_vars_inited(evn_vars_ssv='TOKEN USER_IDS', trace=True):
    log.debug(f"""
        {(xxx := all_([
        (bool(os.getenv(a, '')),
         (print if trace else lambda _: _)
             (
             f"{a = }; "
             f"{bool(os.getenv(a, '')) = }; "
         )
         )[0]
        for a in evn_vars_ssv.split()
        ])) = }
    """)
    return bool(os.getenv('TOKEN'))
    # todo: test 1st:
    return xxx


# @_log_call
def env_setdefaults_by_args(args: Namespace) -> None:
    log.info(
        f"""# Initialize environment variables, if not already set by 
{args = }"""
    )
    log.debug(f"""
        {vars(args) =}""")

    # for k, v in dict(args).items():
    for k, v in vars(args).items():
        log.debug(f""">
        os.environ.setdefault({k}.upper(), {v})
        """)
        os.environ.setdefault(k.upper(), str(v))

    return None

    # ~? todo:
    os.environ.setdefault("TOKEN", str(args.token))
    os.environ.setdefault("DEBUG", str(args.debug))
    os.environ.setdefault("PORT", str(args.port))
    os.environ.setdefault("USER_IDS", str(args.USER_IDS))
    # todo: add others

    assert args.app_name
    os.environ.setdefault("HEROKU_APP_NAME", str(args.app_name))

    from .asserts import get_env_vars_values
    xxx = get_env_vars_values()
    return xxx
