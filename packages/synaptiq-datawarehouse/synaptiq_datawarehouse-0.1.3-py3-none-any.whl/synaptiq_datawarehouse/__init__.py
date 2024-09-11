import os
from pathlib import Path
from typing import Any, Dict

import yaml

def hello() -> str:
    return "Hello from synaptiq-datawarehouse!"

class DotDict(Dict[str, Any]):
    """
    Dictionary (nested) with dot notation with type hinting.

    Example:
        >>> config = dotdict({'a': 1, 'b': {'c': 2, 'd': 3}})
        >>> config.a
        1
        >>> config.b.c
        2
        >>> config.b.d
        3
    """

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = DotDict(value)

    def dict(self):
        """
        Converts all dotdicts to dicts.
        """
        d = {}
        for key, value in self.items():
            if isinstance(value, DotDict):
                d[key] = value.dict()
            else:
                d[key] = value
        return d


def load_config(env: str) -> DotDict:
    path = Path(__file__).parent.absolute() / "config"

    with open(path / f"{env}.yaml", "r") as config_file:
        config_dict = yaml.safe_load(config_file)
    config = DotDict(config_dict)
    return config


env = os.environ.get("ENV", "prod").lower()
config = load_config(env)