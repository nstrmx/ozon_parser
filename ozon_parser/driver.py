from typing import Any, List, Optional

import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from settings import LOADING_TIMEOUT
from utils import log




class Driver(webdriver.Firefox):
    
    def __init__(   self,
                    *args,
                    loading_timeout = LOADING_TIMEOUT,
                    headless: bool = True, 
                    options: Optional[Options] = None, 
                    **kwargs):
        log(f"Starting webdriver" + " headless" if headless == True else '')

        if options is None:
            options = Options()
            options.headless = headless

        webdriver.Firefox.__init__(self, *args, options=options, **kwargs)

        self.loading_timeout = loading_timeout

    
    def get_url(self, url: str):
        log(f"Getting url: {url}")
        self.get(url)

        
    def scroll_to_bottom(self):
        log("Scrolling to bottom of the page")

        old_scroll_height = -1
        new_scroll_height = self.execute_script("return document.body.scrollHeight;")
        
        while old_scroll_height < new_scroll_height:
            self.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(self.loading_timeout)
            
            old_scroll_height = new_scroll_height
            new_scroll_height = self.execute_script("return document.body.scrollHeight;")


    def get_next_pages(self, xpath_selector) -> List[str]:
        log("Getting number of pages")

        page_num_links = self.xpath_all(xpath_selector)
        page_num_links = [*map(self.selectors.page_num_links.format, page_num_links)] 
        
        log(f"{len(page_num_links)} pages to walk through")
        return page_num_links


    def xpath(self, path: str) -> Any:
        return self.execute_script("""return {
            var contextNode = document;
            var nsResolver = document.createNSResolver( contextNode.ownerDocument == null ? contextNode.documentElement : contextNode.ownerDocument.documentElement );
            var result = document.evaluate(%s, contextNode, nsResolver, XPathResult.ORDERED_NODE_ITERATOR_TYPE, null);
            return result.iterateNext();
        }
        """ % path)
        #return self.find_element(By.XPATH, path)


    def xpath_all(self, path: str) -> Any:
        return self.find_elements(By.XPATH, path)