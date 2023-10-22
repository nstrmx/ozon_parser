import logging
import time
from random import randint
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from settings import LOADING_TIMEOUT, HEADLESS, WEBDRIVER_PATH


log = logging.getLogger("default")


class Driver(webdriver.Firefox):
    loading_timeout = LOADING_TIMEOUT
    headless = HEADLESS
    webdriver_path = WEBDRIVER_PATH

    def __init__(self, **kwargs):
        options = kwargs.pop("options", None)
        service = Service(executable_path=self.webdriver_path)
        if options is None:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
        webdriver.Firefox.__init__(self, service=service, options=options)

    def __enter__(self):
        log.debug(f"Starting webdriver" + " in headless mode" if self.headless == True else '')
        return super().__enter__()

    def __exit__(self, *args):
        log.debug(f"Closing webdriver")
        self.quit()
        return super().__exit__(*args)
    
    def get_url(self, url: str):
        log.debug(f"Getting url: {url}")
        self.get(url)
        
    def scroll_to_bottom(self):
        log.debug("Scrolling to bottom of the page")
        old_scroll_height = -1
        new_scroll_height = self.execute_script("return document.body.scrollHeight;")
        while old_scroll_height < new_scroll_height:
            self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(self.loading_timeout)
            old_scroll_height = new_scroll_height
            new_scroll_height = self.execute_script("return document.body.scrollHeight;")

    def generate(self, url: str):
        link = ""
        while link is not None:
            self.get_url(url+link)
            self.scroll_to_bottom()
            link = yield self.page_source
            