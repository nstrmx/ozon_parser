import importlib
from operator import imod
from typing import List,Callable

from dataclasses import dataclass




def bypass(_: List = []) -> List: 
    return _
    

@dataclass
class Selector:
    xpath: str
    handle: Callable