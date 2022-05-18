from typing import List, Tuple, Union


from dataclasses import dataclass
from argparse import Namespace

from lxml.etree import HTML, XPathEvalError, Element
from selenium.webdriver.common.by import By

from settings import WARNING, Selector
from utils import exception_handler, default_handler, log
from ozon_parser.driver import Driver

 
        

def parse_value_handler(exception, message, self, _, key, selector):
        default_handler(exception, message)
        setattr(self, key, selector.handle())


@dataclass
class ProductData:

    def __init__(self, values: Tuple, selectors: Namespace):
        
        for key, value in zip(selectors.__dict__.keys(), values):
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
    """
    def __init__(self, source: str, selectors: Namespace = SELECTORS.page):
        self.source = source
        self.selectors = selectors
    """

    def get_html(self) -> Element:
        return HTML(self.source)


    def get_next_pages(self, html, selector) -> List[str]:
        log("Getting number of pages")

        page_num_links = self.xpath(html, selector)
        
        log(f"{len(page_num_links)} pages to walk through")
        return page_num_links


    def parse_page(self, page_num: int=0) -> List[ProductData]:
        if page_num < 1:
            log(f"Parsing page")
        else:
            log(f"Parsing page {page_num}")

        html = self.get_html()

        product_cards = html.xpath(self.selectors.product_card.xpath)

        product_data_list = []

        for i, card in enumerate(product_cards):
            product_data = ProductData(card)
            if product_data.is_empty() == False:
                product_data_list.append(product_data)
            else:
                log(f"product_data[{i}] on page {page_num} is empty. Check if selectors are valid.", level=WARNING)

        if len(product_data_list) == 0:
            log(f"Parsed {len(product_data_list)} products")
        else:    
            log(f"Parsed {len(product_data_list)} products")

        return product_data_list


    def xpath(self, source: Union[Driver, etree.Element, str], selector: Selector):
        return self.xpath_with_lxml(source, selector)

    
    def xpath_with_driver(self, driver, selector):
        value = driver.find_elements(By.XPATH, selector.xpath)
        return selector.handle(value)


    # TODO: add exception handler that returns default value
    def xpath_with_lxml(self, html: Union[etree.Element, str], selector):
        try:
            if isinstance(html, str):
                html = etree.HTML(html)
            value = html.xpath(selector.xpath)
            log(value)
            return selector.handle(value)
        except Exception as e:
            log(e, level=WARNING)
            return selector.handle()





def main():
    from settings import WEBDRIVER_PATH, HEADLESS, SHOP_URL, SELECTORS

    with Driver(executable_path=WEBDRIVER_PATH, headless=HEADLESS) as driver:

        driver.get_url(SHOP_URL)
        driver.scroll_to_bottom()

        parser = Parser()

        html = etree.HTML(driver.page_source)

        parser.xpath(html, SELECTORS.product.title)
        parser.xpath(html, SELECTORS.product.old_price)
        parser.xpath(html, SELECTORS.product.new_price)




if __name__ == "__main__":
    main()
