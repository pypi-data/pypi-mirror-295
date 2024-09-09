import os
from datetime import date
from dateutil import parser
from dateutil.parser import ParserError
from pathlib import Path
from typing import Final

# the prefix for the names of the environment variables
APP_PREFIX: Final[str] = os.getenv("PYPOMES_APP_PREFIX", "")


def env_get_str(key: str,
                def_value: str = None) -> str:
    """
    Retrieve and return the string value defined for *key* in the current operating environment.

    :param key: the key the value is associated with
    :param def_value: the default value to return, if the key has not been defined
    :return: the string value associated with the key
    """
    result: str = os.getenv(key)
    if result is None:
        result = def_value

    return result


def env_get_bool(key: str,
                 def_value: bool = None) -> bool:
    """
    Retrieve and return the boolean value defined for *key* in the current operating environment.

    These are the criteria:
        - case is disregarded
        - the string values accepted to stand for *True* are *1*, *t*, or *true*
        - the string values accepted to stand for *False* are *0*, *f*, or *false*
        - all other values causes *None* to be returned

    :param key: the key the value is associated with
    :param def_value: the default value to return, if the key has not been defined
    :return: the boolean value associated with the key, or 'None' if a boolean value could not be established
    """
    result: bool | None
    try:
        if os.environ[key].lower() in ["1", "t", "true"]:
            result = True
        elif os.environ[key].lower() in ["0", "f", "false"]:
            result = False
        else:
            result = None
    except (AttributeError, KeyError, TypeError):
        result = def_value

    return result


def env_get_date(key: str,
                 def_value: date = None) -> date:
    """
    Retrieve and return the date value defined for *key* in the current operating environment.

    :param key: the key the value is associated with
    :param def_value: the default value to return, if the key has not been defined
    :return: the date value associated with the key
    """
    result: date
    try:
        result = parser.parse(os.environ[key]).date()
    except (AttributeError, KeyError, TypeError, ParserError, OverflowError):
        result = def_value

    return result


def env_get_int(key: str,
                def_value: int = None) -> int:
    """
    Retrieve and return the integer value defined for *key* in the current operating environment.

    :param key: the key the value is associated with
    :param def_value: the default value to return, if the key has not been defined
    :return: the integer value associated with the key
    """
    result: int
    try:
        result = int(os.environ[key])
    except (AttributeError, KeyError, TypeError):
        result = def_value

    return result


def env_get_float(key: str,
                  def_value: float = None) -> float:
    """
    Retrieve and return the float value defined for *key* in the current operating environment.

    :param key: the key the value is associated with
    :param def_value: the default value to return, if the key has not been defined
    :return: the float value associated with the key
    """
    result: float
    try:
        result = float(os.environ[key])
    except (AttributeError, KeyError, TypeError):
        result = def_value

    return result


def env_get_path(key: str,
                 def_value: Path = None) -> Path:
    """
    Retrieve and return the path value defined for *key* in the current operating environment.

    :param key: the key the value is associated with
    :param def_value: the default value to return, if the key has not been defined
    :return: the path value associated with the key
    """
    result: Path
    try:
        result = Path(os.environ[key])
    except (AttributeError, KeyError, TypeError):
        result = def_value

    return result
