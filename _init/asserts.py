import logging
import os

import utils
from _init.util import isiterable
from utils import shorten


# from _init import _log_call


def get_globs_values():
    from . import globals as conf

    return (
        conf.HEROKU_APP_NAME,
        conf.TOKEN,
        conf.DEBUG,
        conf.PORT,
        conf.TIMEOUT,
        conf.USER_IDS,
    )


def get_globs_names(): return (
    'HEROKU_APP_NAME TOKEN DEBUG PORT TIMEOUT USER_IDS'.split()
)


def get_globs(): return dict(zip(
    get_globs_names(),
    get_globs_values(),
))


def assert_globs():
    assert_all(
        *get_globs_values(),
        args=get_globs_names(),
        trace=True,
    )
    utils.log.info(f"All globs're checked: "
                   f"{get_globs_names() = }; "
                   f"{get_globs_values() = }; "
                   f"")


def get_env_vars_list():
    return 'TOKEN PORT USERS_IDS URL'.split()


def get_env_vars_dict(): return {
    v: os.getenv(v) for v in get_env_vars_list()
}


def get_env_vars_values(): return (
    os.getenv('TOKEN')
    , os.getenv('DEBUG')
    , int(os.getenv('PORT'))
    , int(os.getenv('TIMEOUT'))
    , (os.getenv('USER_IDS'))
    # , (os.getenv('URL'))
    # , os.getenv('HEROKU_APP_NAME')
)


# @_log_call
def assert_env_vars():
    xxx = get_env_vars_values()
    assert_all(*xxx)
    # return True
    # todo: test 1st!!
    # assert_all(
    #     **get_env_vars_dict(),
    #     trace=True,
    # )
    utils.log.info(
        f"All env_vars're checked: "
        f"{({k: os.getenv(k) for k in get_env_vars_dict().keys()})};"
        f"👌")

    return xxx


def assert_file(config_file):
    assert os.path.isfile(config_file), f"No file <{config_file}>!"
    return config_file


def all_(*a, args=None, print=print):
    if not all(a):
        print(f"Not all! {f'{args}:' if args else ''} {a}")
    return all(a)
    # if all(a): return a
    # else:
    #     log.debug()


def assert_all(*a, args=None, trace=False, **kwargs):
    if len(a) == 1:
        if isiterable(a):
            logging.debug(f"# ! <{shorten(a[0], 333)=}>'ll be analysed:..")
    aargs, aa = '', None
    if kwargs:
        aa = list(a)
        aa += kwargs.values()
        if not aargs:
            aargs = ['?'] * len(aa)
        aargs += type(aargs)(kwargs.keys())

    msg = f"all {f'{args}: ' if args else ''}{a}"
    assert all(a), f"Not {msg}!"

    if aa is not None:
        amsg = f"all {f'?: ' if aargs else ''}{aa}"
        assert all(aa), f"Not {amsg}!"

    assert all(kwargs.values()), f"Not all {kwargs.values() = }!"

    if trace: logging.debug(f"Args good {msg} 👌")
    return a
