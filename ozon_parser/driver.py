from typing import Any, List, Optional

import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from settings import LOADING_TIMEOUT, Selector
from utils import log




class Driver(webdriver.Firefox):
    
    def __init__(   self,
                    *args,
                    loading_timeout = LOADING_TIMEOUT,
                    headless: bool = True, 
                    options: Optional[Options] = None, 
                    **kwargs):
        
        self.__headless = headless
        self.loading_timeout = loading_timeout

        if options is None:
            options = Options()
            options.headless = self.__headless

        webdriver.Firefox.__init__(self, *args, options=options, **kwargs)


    def __enter__(self):
        log(f"Starting webdriver" + " in headless mode" if self.__headless == True else '')
        return super().__enter__()


    def __exit__(self, *args):
        log(f"Closing webdriver")
        self.quit()
        return super().__exit__(*args)

    
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




def main():
    from settings import WEBDRIVER_PATH

    with Driver(executable_path=WEBDRIVER_PATH) as driver:
        driver.get_url("https://google.com")

        n = 15

        while n:
            print(n)
            time.sleep(1)
            n -= 1
            if n == 10:
                1 / 0

    print("Hello world")


if __name__ == "__main__":
    main()