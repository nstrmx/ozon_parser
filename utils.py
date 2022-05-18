from typing import Any, Union, Optional, List, Tuple, Dict, Callable, NewType
from types import FunctionType

from datetime import datetime
from functools import partial
from argparse import Namespace
from pprint import pprint

from settings import LOGGING_ENABLED, LEVELS, INFO, ERROR, VERBOSITY_LEVEL




types = Namespace()
ExceptionArgs = NewType('ExceptionArgs', Tuple[Exception])
ExceptionHandler = Callable[[ExceptionArgs, str], Any]


def partial_wrapper(*part_args, **part_kwargs):
    def wrapper_func(func):
        return partial(func, *part_args, **part_kwargs)
    return wrapper_func



def __log(*args,
        enabled: bool       = True, 
        levels: List[str]   = [],
        level: int          = 0,
        verbosity: int      = 0,
        printer: Callable   = print,
        **kwargs):
    """
    parameters
        level: indicates given level of a log message
        verbosity: only messages with given (and higher) verbosity level will be displayed
        levels: list of log level names to work with
        debug: enables/disables logging
    """

    if enabled == True:
        if level >= verbosity:
            print(f"[{datetime.now()}][{levels[level]}]:", end=' ')
            printer(*args, **kwargs)


def log(*args, **kwargs):
    return __log(*args, 
                 enabled = LOGGING_ENABLED, 
                 verbosity = VERBOSITY_LEVEL, 
                 levels = LEVELS, 
                 **kwargs)


def hasmethod(obj: Any, method_name: str) -> bool:
    return hasattr(obj, method_name) and callable(getattr(obj, method_name))
    

def default_handler(exception: Exception, message: str) -> Any:
    exception_name = str(exception)
    log(f"({exception_name})", message, level=ERROR)


def exception_handler(exception: Union[Exception, FunctionType] = Exception, 
                      handler: ExceptionHandler = default_handler) -> Callable:

    __func: FunctionType = lambda *args, **kwargs: None

    def wrapper_proc(*args, **kwargs) -> Any:
        nonlocal exception
        nonlocal handler
    
        try:
            return __func(*args, **kwargs)
        except exception as e:
            return handler(exception, e, *args, **kwargs)
            

    def wrapper_func(func: Callable) -> FunctionType:
        nonlocal __func

        __func = func
        return wrapper_proc
        
    
    if isinstance(exception, FunctionType):
        __func = exception
        exception = Exception
        return wrapper_proc

    return wrapper_func


def response_printer(*args, **kwargs):
    print()
    pprint(*args, **kwargs)