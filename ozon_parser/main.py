import logging
from ozon_parser.driver import Driver
from ozon_parser.parser import Parser
from ozon_parser.database import Database
from ozon_parser.sheets import Sheet
from settings import SHOP_URL


log = logging.getLogger("default")


def main():
    parser = Parser()
    sheets = Sheet()
    database = Database()
    with Driver() as driver:
        # Getting html from shop pages
        page_itr = driver.generate(SHOP_URL)
        # Parsing product cards
        data_itr = parser.generate(page_itr)   
        # Saving data to database
        data_itr = database.generate(data_itr) 
        # Adding data to google sheets
        data_itr = sheets.generate(data_itr)
        # Consume
        list(data_itr)
       