from typing import Any


def hasmethod(obj: Any, method_name: str) -> bool:
    return hasattr(obj, method_name) and callable(getattr(obj, method_name))
