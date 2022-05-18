from typing import Callable

from argparse import Namespace
from dataclasses import dataclass




DEBUG = True
LOGGING_ENABLED = True


# utils.py
## LOGGING
LEVELS = ["INFO", "WARNING", "ERROR"]
INFO = 0
WARNING = 1
ERROR = 2
VERBOSITY_LEVEL = INFO


# ozon_parser/driver.py
## DRIVER

WEBDRIVER_PATH = "/home/ckr/.webdrivers_for_selenium/geckodriver"
HEADLESS = True
LOADING_TIMEOUT = 0.75
SHOP_URL = "https://www.ozon.ru/seller/skyfors-301871/products/?miniapp=seller_301871"


# ozon_parser/parser.py
## PARSER

@dataclass
class Selector:
    xpath: str
    format: Callable

SELECTORS = Namespace(
    page = Namespace(
        product_card = Selector(
            xpath="""//div[starts-with(@data-widget, "megaPaginator")]//*[starts-with(@class, "widget-search-result-container")][1]/div[1]/div""",
            format=lambda _: _ or ''
        ),
        page_num_links = Selector(
            xpath="""//div[starts-with(@data-widget, "megaPaginator")]/div[2]//a/@href""",
            format=str
        ),
    ),    
    product = Namespace(
        title = Selector(
            xpath = """//div[1]/a[starts-with(@class, "tile-hover-target")]//text()""",
            format=str
        ),
        old_price = Selector(
            xpath="""//div[1]/div[1]/span[2]//text()""",
            format=str
        ),
        new_price = Selector(
            xpath="""//div[1]/div[1]/span[1]//text()""",
            format=str
        ),
        discount = Selector(
            xpath="",
            format=str
        ),
    ),
)


# ozon_parser/sheet.py
## SPREADSHEETS 
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
CREDS_PATH = "credentials.json"
SHEETS_API_VERSION = "v4"
SHEET_ID = "1_8CYhuQvkCVMJcBSD9EbkpNYPEr1VTdiOwSc2S45KdY"
