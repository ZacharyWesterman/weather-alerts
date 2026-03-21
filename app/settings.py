import json
from typing import Any

with open('config/settings.json', 'r') as fp:
    __CONFIG = json.load(fp)


def get(key: str) -> Any:
    global __CONFIG
    return __CONFIG.get(key)
