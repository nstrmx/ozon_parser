from typing import List, Optional

import time
from dataclasses import dataclass
from argparse import Namespace

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from bs4.element import Tag
from bs4 import BeautifulSoup as Soup

from settings import LOADING_TIMEOUT, SELECTORS
from utils import log




class Driver(webdriver.Firefox):
    def __init__(   self,
                    *args,
                    loading_timeout = LOADING_TIMEOUT,
                    headless: bool = True, 
                    options: Optional[Options] = None, 
                    **kwargs):
        log("Starting webdriver")

        if options is None:
            options = Options()
            options.headless = headless

        webdriver.Firefox.__init__(self, *args, options=options, **kwargs)

        self.loading_timeout = loading_timeout
        
    def scroll_to_bottom(self):
        log("Scrolling to bottom of the page")

        old_scroll_height = -1
        new_scroll_height = self.execute_script("return document.body.scrollHeight;")
        
        while old_scroll_height < new_scroll_height:
            self.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(self.loading_timeout)
            
            old_scroll_height = new_scroll_height
            new_scroll_height = self.execute_script("return document.body.scrollHeight;")    
        

@dataclass
class ProductData:
    def __init__(self, card: Tag, selectors:  Namespace):
        self.is_empty = True

        for key, selector in selectors.__dict__.items():
            selection = card.select(selector)
            if len(selection) > 0:
                self.is_empty = False
                if len(selection) == 1:
                    setattr(self, key, selection[0].text)
                else:
                    setattr(self, key, [item.text for item in selection])

    def __str__(self):
        body = []
        for key, value in self.__dict__.items():
            if key != "is_empty":
                body.append(f"{key} = {value}")

        return "ProductData(" + (", ".join(body)) + ")"

    def get_values(self) -> List[str]:
        values = []
        for key, value in self.__dict__.items():
            if key != "is_empty":
                values.append(str(value))
        return values


class Parser:

    def __init__(self, source: str, selectors: Namespace = SELECTORS):
        self.source = source
        self.selectors = selectors


    def get_html(self) -> Soup:
        return Soup(self.source, "html.parser")


    def get_number_of_pages(self, html: Optional[Tag] = None) -> int:
        log("Getting number of pages")

        if html == None:
            html = self.get_html()

        page_numbers = html.select(self.selectors.page_numbers)
        number_of_pages = len(page_numbers)
        
        log(f"{number_of_pages} pages to walk through")
        return number_of_pages


    def parse_page(self, page_num: int=0) -> List[ProductData]:
        if page_num < 1:
            log(f"Parsing page")
        else:
            log(f"Parsing page {page_num}")

        html = self.get_html()

        product_cards = html.select(self.selectors.product_card)

        product_data_list = []

        for card in product_cards:
            product_data = ProductData(card, self.selectors.product_data)
            if product_data.is_empty == False:
                product_data_list.append(product_data)

        return product_data_list




def main():
    pass




if __name__ == "__main__":
    main()
