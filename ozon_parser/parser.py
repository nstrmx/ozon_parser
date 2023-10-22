from typing import List, Generator
import re
import logging
from dataclasses import dataclass
from bs4 import BeautifulSoup
from ozon_parser import selectors


log = logging.getLogger("default")
 

@dataclass
class ProductData:
    title: str
    old_price: int
    new_price: int
    discount: float

    def get_values(self) -> List[str]:
        return list(self.__dict__.values())

class Parser:
    def parse_tree(self, source: str) -> BeautifulSoup:
        return BeautifulSoup(source, "html.parser")

    def select_int(self, tree: BeautifulSoup, selector: str, default: int = 0) -> int:
        try:
            tag = tree.select_one(selector)
            val = re.sub(r"[^0-9]+", "", tag.text)
            return int(val)
        except (AttributeError, ValueError, IndexError) as e:
            log.error("error parsing selector %s: %s" % (selector, e))
            return default
        
    def select_str(self, tree: BeautifulSoup, selector: str, default: str = "") -> str:
        try:
            tag = tree.select_one(selector)
            val = tag.text.strip()
            return val
        except (AttributeError, ValueError) as e:
            log.error("error parsing selector %s: %s" % (selector, e))
            return default

    def select_href(self, tree: BeautifulSoup, selector: str, default: str = "") -> str:
        try:
            tag = tree.select_one(selector)
            href = tag.get("href")
            return href
        except (AttributeError, ValueError) as e:
            log.error("error parsing selector %s: %s" % (selector, e))
            return default

    def parse_page(self, tree: BeautifulSoup) -> Generator[ProductData, None, None]:
        product_items = tree.select(selectors.product_items)
        num_of_products = len(product_items)
        if num_of_products == 0:
            return
        for i in range(1, num_of_products+1):
            product_data = ProductData(
                title=self.select_str(tree, selectors.title % i), 
                old_price=self.select_int(tree, selectors.old_price % i), 
                new_price=self.select_int(tree, selectors.new_price % i),
                discount=self.select_int(tree, selectors.discount % i) / 100,    
            )
            yield product_data
    
    def generate(self, page_itr: Generator[str, str, None]) -> Generator[ProductData, None, None]:
        try:
            page = next(page_itr)
        except StopIteration:
            return
        while True:
            tree = self.parse_tree(page)
            yield from self.parse_page(tree)
            next_page_link = self.select_href(tree, selectors.next_page)
            if not next_page_link:
                break
            m = re.search(r"(\?page=\d+)$", next_page_link)
            if m:
                page = page_itr.send(m.group())
            