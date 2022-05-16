from typing import List

from datetime import datetime
from string import ascii_uppercase as abc
from pprint import pprint

from ozon_parser.sheets import GoogleService
from ozon_parser.parser import Driver, Parser, ProductData

from settings import CREDS_PATH, SCOPES, WEBDRIVER_PATH, SHEET_ID, SHEETS_API_VERSION, SHOP_URL



def main():
    # Getting data from shop page
    driver = Driver(executable_path=WEBDRIVER_PATH)

    driver.get(SHOP_URL)
    driver.scroll_to_bottom()

    data: List[ProductData] = [] 

    parser = Parser(driver.page_source)
    data.extend(parser.parse_page())

    number_of_pages = parser.get_number_of_pages()

    if number_of_pages > 1:

        for i in range(2, number_of_pages + 1):
            driver.get(SHOP_URL + f"&page={i}")
            driver.scroll_to_bottom()
            
            parser = Parser(driver.page_source)
            data.extend(parser.parse_page(i))
            
    driver.quit()

    table: List[List[str]] = []
    
    for i, item in enumerate(data, 1):
        row = [str(i), *item.get_values(), str(datetime.now())]
        table.append(row)

    # Adding data to google sheets
    service = GoogleService(CREDS_PATH, SCOPES)
    sheets = service.build_sheets(SHEETS_API_VERSION, SHEET_ID)

    number_of_columns = len(max(table, key=lambda row: len(row)))
    number_of_rows = len(table)

    sheet_range = f"Лист1!A2:{abc[number_of_columns]}{number_of_rows + 2}"

    response = sheets.batch_update(sheet_range, table)
    pprint(response)

    response = sheets.get_range(sheet_range)
    pprint(response)


if __name__ == "__main__":
    main()
