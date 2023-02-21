from typing import Optional, Any

import yaml


# @_log_call
# from: /Users/user/github.com/hnkovr/`MyPrjsReview1/my_fastapi_app/heroky/yaml_loader.py
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


def load_config(config_file):
    """Load configuration from a YAML file."""
    from _init.asserts import assert_file

    assert_file(config_file)
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    return config


def save_defaults_to_yaml(file_path):
    """Save default configuration settings to a YAML file."""
    from _init.init_tools import Defaults

    defaults = {
        "debug": Defaults.DEBUG,
        "port": Defaults.PORT,
        "token": Defaults.TOKEN,
        "app_name": Defaults.HEROKU_APP_NAME,
        "TIMEOUT": 30,
    }
    with open(file_path, "w") as f:
        yaml.dump(defaults, f, default_flow_style=False)
