from typing import List

from datetime import datetime
from string import ascii_uppercase as abc
from itertools import zip_longest

from lxml.etree import HTML

from ozon_parser.driver import Driver
from ozon_parser.sheets import GoogleService
from ozon_parser.parser import Parser, ProductData

from settings import CREDS_PATH, DATA, HEADLESS, SCOPES, SELECTORS, WARNING, WEBDRIVER_PATH, SHEET_ID, SHEETS_API_VERSION, SHOP_URL
from utils import log




def main():

    # Getting html from shop pages
    with Driver(executable_path=WEBDRIVER_PATH, headless=HEADLESS) as driver:

        driver.get_url(SHOP_URL)
        driver.scroll_to_bottom()

        parser = Parser()
        
        html_pages = []

        page = parser.get_html(driver.page_source)
        html_pages.append(page)        

        log("Getting number of pages")
        
        page_num_links = parser.xpath(page, SELECTORS.page_num_links)
        
        if len(page_num_links) > 1:
            log(f"{len(page_num_links)} pages to walk through")

        if len(page_num_links) > 1:

            for i, link in enumerate(page_num_links[1:], 1):
                driver.get_url(SHOP_URL + link)
                driver.scroll_to_bottom()
                
                page = HTML(driver.page_source)
                html_pages.append(page)


    # Parsing product cards

    data: List[ProductData] = []

    for page in html_pages:

        titles     = parser.xpath(page, SELECTORS.product.title)
        old_prices = parser.xpath(page, SELECTORS.product.old_price)
        new_prices = parser.xpath(page, SELECTORS.product.new_price)
        discount   = parser.xpath(page, SELECTORS.product.discount)

        for values in zip_longest(titles, old_prices, new_prices, discount, fillvalue=''):
            data.append(ProductData(values, SELECTORS.product))


    # Formatting data for google sheets

    table: List[List[str]] = []
    
    for i, item in enumerate(data, 1):
        log(item, level=DATA)
        row = [str(i), *item.get_values(), str(datetime.now())]
        table.append(row)

    if len(table) == 0:
        log("Nothing to save. Closing.", level=WARNING)
        return


    # Adding data to google sheets

    service = GoogleService(CREDS_PATH, SCOPES)
    sheets = service.build_sheets(SHEETS_API_VERSION, SHEET_ID)

    sheets.clear_range("Лист1!A2:Z")

    number_of_columns = len(max(table, key=lambda row: len(row)))
    number_of_rows = len(table)

    sheet_range = f"Лист1!A2:{abc[number_of_columns]}{number_of_rows + 2}"

    sheets.batch_update(sheet_range, table)
    
    sheets.get_range(sheet_range)




if __name__ == "__main__":

    main()
