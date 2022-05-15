from itertools import product
import os.path, time

import selenium as sl
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup as Soup

from settings import WEBDRIVER_PATH, LOADING_TIMEOUT

SHOP_URL = "https://www.ozon.ru/seller/skyfors-301871/products/?miniapp=seller_301871"


def init_driver(headless=True):
    options = Options()
    options.headless = headless

    driver = webdriver.Firefox(
        options=options,
        executable_path=WEBDRIVER_PATH
    )

    return driver

def parse(driver, url):
    driver.get(url)
    time.sleep(LOADING_TIMEOUT)
    #TODO: add scroll down to bottom of the page

    page_source = driver.page_source
    html = Soup(page_source, "html.parser")

    container = html.select(".widget-search-result-container")[0]
    product_cards = container.select("div > div")

    return [card.text for card in product_cards]


def main():
    driver = init_driver()

    data = parse(driver, SHOP_URL)
    print(*data, sep="\n")


if __name__ == "__main__":
    main()