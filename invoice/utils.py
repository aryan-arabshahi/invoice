from typing import Any
from os import getenv


def env(key: str, default_value: Any = None) -> Any:
    """Get the variable from the environment

    Arguments:
        key (str) -- The specific key

    Keyword Arguments:
        default_value (Any) -- The default value (default None)
    """
    return getenv(key, default_value)
