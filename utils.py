from typing import Any, Type, List, Callable
from types import FunctionType

from datetime import datetime
from pprint import pprint

from settings import INFO, LOGGING_ENABLED, LEVELS, ERROR, VERBOSITY_LEVEL




def log(*args,
        enabled: bool       = LOGGING_ENABLED, 
        levels: List[str]   = LEVELS,
        level: int          = INFO,
        verbosity: int      = VERBOSITY_LEVEL,
        printer: Callable   = print,
        **kwargs):

    if enabled == True:
        if level >= verbosity:
            print(f"[{datetime.now()}][{levels[level]}]:", end=' ')
            printer(*args, **kwargs)


def hasmethod(obj: Any, method_name: str) -> bool:
    return hasattr(obj, method_name) and callable(getattr(obj, method_name))
    

def default_handler(exception: Exception, *args, **kwargs) -> Any:
    name = type(exception).__name__
    log(f"({name})", str(exception), level=ERROR)


def exception_handler(*args, 
                      exception: Type[Exception] = Exception, 
                      handler: Callable = default_handler) -> Callable:

    __func = lambda *args, **kwargs: None
    
    flag_skip = False

    # TODO: add more suitable callable types
    if len(args) > 0 and isinstance(args[0], FunctionType):
        __func = args[0]
        flag_skip = True
    elif len(args) > 1 and isinstance(args[1], FunctionType):
        __func = args[1]
        flag_skip = True


    def wrapper_proc(*args, **kwargs) -> Any:
        nonlocal exception
        nonlocal handler
    
        try:
            return __func(*args, **kwargs)
        except exception as e:
            return handler(e, *args, **kwargs)
            

    def wrapper_func(func: Callable) -> Callable:
        nonlocal __func

        __func = func
        return wrapper_proc
        
    return wrapper_proc if flag_skip else wrapper_func


def response_printer(*args, **kwargs):
    print()
    pprint(*args, **kwargs)