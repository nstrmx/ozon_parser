from typing import Any

import datetime as dt
from settings import DEBUG, VERBOSE_LOG



def log(*args, level: str = "INFO", **kwargs):
    if DEBUG == True and VERBOSE_LOG == True:
        print(f"[{dt.datetime.now()}][{level}]:", *args, **kwargs)

def hasmethod(obj: Any, method_name: str) -> bool:
    return hasattr(obj, method_name) and callable(getattr(obj, method_name))
