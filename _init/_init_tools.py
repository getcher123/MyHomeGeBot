# i from _init import _log_call
# @_log_call
import logging


# from _init import _log_call
# @_log_call(with_call_stack=True)
# ImportError: cannot import name '_log_call' from partially initialized module '_init' (most likely due to a circular import) (/Users/user/github.com/getcher123/MyHomeGeBot/_init/__init__.py)

def assert_all(*a, args=None, trace=False):
    msg = f"all {f'{args}: ' if args else ''}{a}"
    assert all(a), f"Not {msg}!"
    if trace: logging.debug(f"Args good {msg} 👌")
    return a
