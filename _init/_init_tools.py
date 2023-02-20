# i from _init import _log_call
# @_log_call
def assert_all(*a, args=None):
    assert all(a), f"{f'{args}: ' if args else ''}{a}"
