from typing import Any, List, Tuple, Type, Union

from dataclasses import dataclass
from argparse import Namespace

from lxml.etree import HTML
from selenium.webdriver.common.by import By

from settings import DATA, Selector
from utils import exception_handler, default_handler, log
from ozon_parser.driver import Driver

 

# dirty patch to resolve pytype [import-error]     
element = HTML("<html></html>")
Element = type(element)
try:
    element.xpath("")
except Exception as e:
    XPathEvalError = type(e)


def xpath_handler(exception: Exception, _1, _2, selector, *args, **kwargs) -> Any:
    default_handler(exception)
    return selector.handle()


@dataclass
class ProductData:

    def __init__(self, values: Tuple, selectors: Namespace):
        
        for key, value in zip(selectors.__dict__.keys(), values):
            if len(value) > 0:
                setattr(self, key, value)
            else:
                setattr(self, key, value)


    def __str__(self):
        body = []
        for key, value in self.__dict__.items():
            body.append(f"{key} = {value}")

        return "ProductData(" + (", ".join(body)) + ")"    


    def get_values(self) -> List[str]:
        return list(self.__dict__.values())


    def is_empty(self) -> bool:
        return len(self.get_values()) == 0




class Parser:
    
    def get_html(self, source) -> Type[Element]:
        return HTML(source)


    def xpath(self, source: Union[Driver, Element, str], selector: Selector):
        return self.xpath_with_lxml(source, selector)

    
    def xpath_with_driver(self, driver, selector):
        value = driver.find_elements(By.XPATH, selector.xpath)
        log(value, level=DATA)
        return selector.handle(value)


    @exception_handler(exception=XPathEvalError, handler=xpath_handler)
    def xpath_with_lxml(self, html: Union[Element, str], selector):
        if isinstance(html, str):
            html = self.get_html(html)
        value = html.xpath(selector.xpath)
        log(value, level=DATA)
        return selector.handle(value)




def main():
    pass




if __name__ == "__main__":
    main()
