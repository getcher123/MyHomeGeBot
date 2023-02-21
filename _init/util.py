import logging
from typing import Callable, Union, Tuple, Any, Type

logd = logging.debug
logd = print


def try_(f: Callable, if_err_fn: Callable, *, except_: Union[Exception, Tuple[Exception]] = Exception,
         if_ok_return: Any = None):
    """
    >>> def f(): return try_(lambda: 1/1, lambda: False, if_ok_return=1)
    >>> print(f())
    1
    >>> def f(): return try_(lambda: 1/0, lambda: False, if_ok_return=1)
    >>> print(f())
    False
    """

    try:
        res = f()
        return if_ok_return if if_ok_return is not None else res
    except except_:
        return if_err_fn()


def deco_with_args(_func=None, *deco_args, log=print, **deco_kwargs):
    """
    >>> import pprint as print
    >>> @deco_with_args(log=print)
    >>> def f(a): print(a)
    ({'a': 1, 'b': 2, 'c': 3},
     {'a': 1, 'b': 2, 'c': 3},
     {'a': 1, 'b': 2, 'c': 3},
     {'a': 1, 'b': 2, 'c': 3})
    """
    log(f"{deco_with_args.__name__}({_func.__name__},"
        f" *{deco_args=}, **{deco_kwargs=})")

    def decorator(func):
        def wrapper(*args, **kwargs):
            log(f"{func.__name__}("
                f" *{args=}, **{kwargs=})")
            return func(*args, **kwargs)

        return wrapper

    return decorator if _func is None else decorator(_func)


def is_not_exc(except_):
    """
    >>> @is_not_exc
    >>> def f(): 1/0
    >>> print(f())
    ?
    """

    def deco(f):
        def w(*a, **k):
            return try_(lambda: f(*a, **k),
                        if_err_fn=lambda: False,
                        if_ok_return=True,
                        except_=except_,
                        )

        return w

    return deco


@is_not_exc(except_=(AssertionError, TypeError))
def isiterable(a, except_types: Tuple[Type] = None):
    """
    >>> [print(a, isiterable(a, except_types=str))
    ...    for a in (None, 1, 'a', 'ab', (), (None,), (1, 2))]
    1
    None False
    1 False
    a False
    ab False
    () True
    (None,) True
    (1, 2) True
    1
    """
    if not isinstance(except_types, tuple): except_types = except_types,
    assert not any(except_types) or not isinstance(a, except_types)
    (e for e in a)


@deco_with_args
def tests():
    [print(a, isiterable(a, except_types=str))
     for a in (None, 1, 'a', 'ab', (), (None,), (1, 2))
     ]
    # for a in (None, 1, 'a', 'ab', (), (None,), (1, 2)):
    #     try:
    #         print(a, iter(a))
    #     except Exception as e:
    #         print(a, str(e), sep='\t')


if __name__ == '__main__':
    # tests()
    # doctest.testmod()

    from pprint import pprint as print

    print((dict(a=1, b=2, c=3),) * 4)

    # log(f"""{a = }\n{
    # (e for e in a)
    # = }""")
