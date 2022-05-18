from typing import List

from datetime import datetime
from string import ascii_uppercase as abc
from pprint import pprint

from ozon_parser.driver import Driver
from ozon_parser.sheets import GoogleService
from ozon_parser.parser import Parser, ProductData

from settings import CREDS_PATH, HEADLESS, SCOPES, SELECTORS, WARNING, WEBDRIVER_PATH, SHEET_ID, SHEETS_API_VERSION, SHOP_URL
from utils import log, response_printer




def main():

    # Getting data from shop page
    with Driver(executable_path=WEBDRIVER_PATH, headless=HEADLESS) as driver:

        driver.get_url(SHOP_URL)
        driver.scroll_to_bottom()

        data: List[ProductData] = [] 

        parser = Parser(driver.page_source)
        items = parser.parse_page()
        
        data.extend(items)

        page_num_links = driver.get_next_pages(SELECTORS.page.page_num_links)

        if len(page_num_links) > 1:

            for i, link in enumerate(page_num_links[1:], 1):
                driver.get_url(SHOP_URL + link)
                driver.scroll_to_bottom()
                
                parser = Parser(driver.page_source)
                items = parser.parse_page(i)

                data.extend(items)


    table: List[List[str]] = []
    
    for i, item in enumerate(data, 1):
        log(item)
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
