import functools
import inspect
import os
from types import FunctionType
from typing import Any, Optional

from loguru import logger as log

from settings import CONF

try:
    from PyYAML import yaml
except ImportError as e:
    log.warning(f"? {e}")
    try:
        import yaml
    except ImportError as e:
        log.warning(f"? {e}")
_logd = print


def get_project_files_names():
    """Return a set of the names of the files in the current project directory."""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    project_files = set()
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.py'):
                project_files.add(os.path.relpath(os.path.join(root, file), dir_path))
    return project_files


def _log_call(func=None, with_call_stack=CONF._log_call_with_call_stack,
              print=log.info
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
                if filename in get_project_files_names():
                    frame_info.append(f"{filename}:{lineno}:{funcname}")
        call_stack_info = ' -> '.join(frame_info) + ' -> ' if with_call_stack else ''
        print(
            # call_stack_info +
            __get_a_kw_call_str(func, args, kwargs))
        result = func(*args, **kwargs)
        if result is not None:
            print(
                call_stack_info +
                f'{pref}{func.__name__} returned: {str(result)[:111]}{"..." if len(str(result)) > 111 else ""}')
        return result

    return wrapper


@_log_call
# /Users/user/github.com/hnkovr/`MyPrjsReview1/my_fastapi_app/heroky/yaml_loader.py
def load_param(
        yaml_file_path,
        param_name: str,
        expected_type: type = str,
        warn_on_missing: bool = True,
        error_on_missing: bool = False,
        error_on_wrong_type: bool = False,
) -> Optional[Any]:
    """
    Load a parameter from the YAML file.

    Args:
        param_name: The name of the parameter to load.
        expected_type: The expected type of the parameter.
        warn_on_missing: If True, print a warning if the parameter is missing. Default is True.
        error_on_missing: If True, raise a KeyError if the parameter is missing. Default is True.
        error_on_wrong_type: If True, raise a TypeError if the loaded parameter is not of the expected type. Default is True.

    Returns:
        The loaded parameter, or None if an error occurred.

    Raises:
        KeyError: If the parameter is missing and error_on_missing is True.
        TypeError: If the loaded parameter is not of the expected type and error_on_wrong_type is True.
    """
    try:
        with open(yaml_file_path, 'r') as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)
    except FileNotFoundError:
        message = f"YAML file '{yaml_file_path = }' not found"
        if error_on_missing:
            raise FileNotFoundError(message)
        elif warn_on_missing:
            print(f"Warning: {message}")
        return None

    if param_name not in yaml_data:
        message = f"Parameter '{param_name}' not found in YAML file '{yaml_file_path}'"
        if error_on_missing:
            raise KeyError(message)
        elif warn_on_missing:
            print(f"Warning: {message}")
        return None

    param_value = yaml_data[param_name]

    if not isinstance(param_value, expected_type):
        message = (
            f"Parameter '{param_name}' in YAML file '{yaml_file_path}' has the wrong type. "
            f"Expected {expected_type}, but got {type(param_value)}"
        )
        if error_on_wrong_type:
            raise TypeError(message)
        else:
            print(f"Warning: {message}")

    return param_value


if __name__ == '__main__':
    @_log_call
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
