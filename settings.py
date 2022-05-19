from argparse import Namespace

from ozon_parser.selectors import bypass, Selector




DEBUG = True

# utils.py
## LOGGING

LOGGING_ENABLED = True

LEVELS = ["DATA", "INFO", "WARNING", "ERROR"]
DATA = 0
INFO = 1
WARNING = 2
ERROR = 3
VERBOSITY_LEVEL = INFO


# ozon_parser/driver.py
## DRIVER

WEBDRIVER_PATH = "/home/ckr/.webdrivers_for_selenium/geckodriver"
HEADLESS = True
LOADING_TIMEOUT = 0.75
SHOP_URL = "https://www.ozon.ru/seller/skyfors-301871/products/?miniapp=seller_301871"


# ozon_parser/parser.py
## PARSER

product_xpath = "//div[starts-with(@data-widget, 'megaPaginator')]//*[starts-with(@class, 'widget-search-result-container')][1]/div[1]/div"
    
SELECTORS = Namespace(

    page_num_links = Selector(
        xpath="//div[starts-with(@data-widget, 'megaPaginator')]/div[2]//a/@href",
        handle=bypass
    ),

    product = Namespace(
        title = Selector(
            xpath = product_xpath + "//a[starts-with(@class, 'tile-hover-target')]//text()",
            handle=bypass
        ),
        old_price = Selector(
            xpath = product_xpath + "//div[1]/div[1]/span[contains(text(), '₽')][1]//text()",
            handle=bypass
        ),
        new_price = Selector(
            xpath = product_xpath + "//div[1]/div[1]/span[contains(text(), '₽')][2]//text()",
            handle=bypass
        ),
        discount = Selector(
            xpath = product_xpath + "//div[1]/div[1]/span[contains(text(), '%')]//text()",
            handle=bypass
        ),
    ),
)


# ozon_parser/sheet.py
## SPREADSHEETS 

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
CREDS_PATH = "credentials.json"
SHEETS_API_VERSION = "v4"
SHEET_ID = "1_8CYhuQvkCVMJcBSD9EbkpNYPEr1VTdiOwSc2S45KdY"
