from argparse import Namespace

DEBUG = True

# utils.py
VERBOSE_LOG = True

# ozon_parser/parser.py

## SELENIUM

WEBDRIVER_PATH = "/home/ckr/.webdrivers_for_selenium/geckodriver"
LOADING_TIMEOUT = 0.5

## PARSER 
SHOP_URL = "https://www.ozon.ru/seller/skyfors-301871/products/?miniapp=seller_301871"

SELECTORS = Namespace(
    product_card = ".widget-search-result-container > div > div",
    product_data = Namespace(
        title = "div.si > a.tile-hover-target.i3q > span.i3q > span",
        old_price = "div.si > div.ui-s2 > span:nth-child(2)",
        new_price = "div.si > div.ui-s2 > span:nth-child(1)",
        discount = "section.q3i > div.i5q > div.qi5 > span:nth-child(1)",
    ),
    page_numbers = "#layoutPage div[data-widget=megaPaginator] > div:nth-child(2) > div > div:nth-child(1) > div:nth-child(1) > a"
)



# ozon_parser/sheet.py

## SPREADSHEETS 
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
CREDS_PATH = "credentials.json"
SHEETS_API_VERSION = "v4"
SHEET_ID = "1_8CYhuQvkCVMJcBSD9EbkpNYPEr1VTdiOwSc2S45KdY"
