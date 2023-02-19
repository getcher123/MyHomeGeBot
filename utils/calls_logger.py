# /Users/user/github.com/hnkovr/__core_logger_copy1.py
import functools
import inspect

inspect
from textwrap import shorten
from types import FunctionType
from typing import Any

from .logger import log

# from core.core import pass_
# from ..loggy._my_logger import logd, get_a_kw_call_str
pass_ = lambda _: _
logd = log.debug
quote = pass_
# from ..core.stringy import shortext
def shortext(s: Any, len=111, **k) -> str:
    """
    >>> shortext('aaabbbcccddddeeee ffffgggghhhhiiiijjjj aaabbbcccdddd eeeeffffgggg hhhhiiii jjjj')
    'aaabbbcccddddeeee ffffgggghhhhiiiijjjj [...] hhhhiiii jjjj'
    """
    if isinstance(s, int) and not isinstance(len, int): a, len = len, s
    return shorten(str(s), len)
    ##!^
    # logging.debug(f"{k.pop('len_tail_percent')=} ignored!")
    # return shorten(str(s), len, **k)
def fmt_arg(a):
    """
    >>> fmt_arg('aaabbbcccddddeeee ffffgggghhhhiiiijjjj aaabbbcccdddd eeeeffffgggg hhhhiiii jjjj')
    "'aaabbbcccddddeeee ffffgggghhhhiiiijjjj [...] eeeeffffgggg hhhhiiii jjjj'"
    """
    return value_shortext(a if not isinstance(a, str) else quote(a))
def fmt_a_or_kw(a):
    """
    >>> fmt_a_or_kw((1, 22, 'aaa'))
    "1, 22, 'aaa'"
    >>> fmt_a_or_kw(dict(a=1, b=22, c='aaabbb cccddddeeeeffff gggghhhh iiii jj jj'))
    "a=1, b=22, c='aaabbb [...] iiii jj jj'"
    """
    return (
        ', '.join(map(fmt_arg, a))
        if isinstance(a, tuple) else
        ', '.join(f"{k}={fmt_arg(v)}" for k, v in a.items())
        if isinstance(a, dict) else '?'
    )
def __get_a_kw_call_str(func: FunctionType, args: tuple, kwargs: dict): return (
    f"> call {func.__name__}{'' if (args and kwargs) else ''}"
    '('
    f"{f' {fmt_a_or_kw(args)}' if args else ''}"
    f"{f', ' if (args and kwargs) else ''}"
    f"{f' {fmt_a_or_kw(kwargs)}' if kwargs else ''}"
    ')->'
)
def __value_shortext(s: Any, len=111,
                     # DEF_LENGHTS.VAR_VALUE,
                     len_tail_percent=0.4) -> str:
    return shortext(s, len, len_tail_percent=len_tail_percent)
get_a_kw_call_str = __get_a_kw_call_str
value_shortext = __value_shortext
# from: _log_args_and_result()
def _log_call(func):
    """
    A decorator that logs the input arguments and the result of the decorated function or method.
    #ChatGPT by created w/o changes (almost))
    """
    print_fn = logd
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print_fn(
            get_a_kw_call_str(func, args, kwargs)
        )
        result = func(*args, **kwargs)
        print_fn(f'> call {func.__name__} returned: {value_shortext(result)}')
        return result
    return wrapper
def _log_call2(with_docstrings=True, with_args_descr=True, use_catch=False, print_fn=print):
    """
    A decorator that logs the input arguments and the result of the decorated function or method.
    """
    logger = loguru.logger if use_catch else None
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            if with_docstrings:
                docstrings = func.__doc__.strip()
                if with_args_descr:
                    arg_spec = inspect.getfullargspec(func)
                    args_desc = ', '.join(f"{a} ({t})" for a, t in zip(arg_spec.args, arg_spec.annotations.values()))
                    docstrings += f"\nArgs: {args_desc}" if args_desc else ""
                print_fn(f"Docstrings: {docstrings}")
            print_fn(get_a_kw_call_str(func, args, kwargs))
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                if logger:
                    logger.catch()
                raise e
            else:
                print_fn(f"> call {func.__name__} returned: {value_shortext(result)}")
                return result
        return inner
    return wrapper
#`?log_call = _log_call2
log_call = _log_call
if __name__ == '__main__':
    @_log_call
    def f(): pass
    f()
    import loguru
    logger = loguru.logger
    @_log_call2(with_docstrings=False, use_catch=True, print_fn=logger.debug)
    def divide(a: int, b: int) -> float:
        """
        Divides a by b.
        """
        return a / b
    divide(4, 2)  # Output: DEBUG:__main__:4 / 2 -> returned: 2.0
    divide(4, 0)  # Output: ERROR:__main__:4 / 0 -> Raised: ZeroDivisionError('division by zero')
