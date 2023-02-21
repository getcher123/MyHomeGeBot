import functools
import inspect
import os
import traceback
from types import FunctionType

from loguru import logger as log

from settings import CONF


def get_project_files_names():
    """Return a set of the names of the files in the current project directory."""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    project_files = set()
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.py'):
                project_files.add(os.path.relpath(os.path.join(root, file), dir_path))
    return project_files


def fmt_txt(e):
    e = str(e)
    return e if not '\n' in e else f"\n{e}\n"


@log.catch
def _log_call(func=None, *, with_call_stack=CONF._log_call_with_call_stack,
              print=log.debug, print_exc=True,
              ):
    pref = '> call '
    pass_ = lambda _: _

    def __get_a_kw_call_str(func: FunctionType, args: tuple, kwargs: dict) -> str:
        return f"{pref}{func.__name__}{'' if (args and kwargs) else ''}" \
               f"({' '.join(str(arg) for arg in args)}, " \
               f"{', '.join(f'{k}={v!r}' for k, v in kwargs.items())}) -> "

    if func is None:
        return functools.partial(_log_call, with_call_stack=with_call_stack)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        frame_info = []
        if with_call_stack:
            for frame in inspect.stack()[1:]:
                filename = frame.filename.split("/")[-1]
                lineno = frame.lineno
                funcname = frame.function
                if (filename in get_project_files_names()
                        and funcname not in 'wrapper '.split()
                        and not (  # todo: optimize
                                'wrapper' in funcname
                        )
                ):
                    frame_info.append(f"{filename}:{lineno}:{funcname}")
        call_stack_info = ' -> '.join(frame_info) + ' -> ' if with_call_stack else ''
        print(
            # call_stack_info +
            __get_a_kw_call_str(func, args, kwargs))
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            if call_stack_info != ' -> ':
                log.error(f"# <{fmt_txt(e)}> while:\n{call_stack_info = }")
            traceback.print_exc() if print_exc else log.exception(
                f"In {_log_call.__name__}({func.__name__}):.."
            )
            log.catch()
            raise

        if result is not None or with_call_stack:
            print(
                call_stack_info +
                f'{pref}{func.__name__} returned: {str(result)[:111]}{"..." if len(str(result)) > 111 else ""}')
        return result

    return wrapper


if __name__ == '__main__':
    # @_log_call
    def add(x: int, y: int) -> int:
        """
        Adds two numbers and returns the result.

        >>> add(2, 3)
        > call add(2 3, ) ->
        > call add returned: 5
        5

        """
        return x + y


    import doctest

    doctest.testmod()
