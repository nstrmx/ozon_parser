import sys
import logging
from logging import config as logging_config
from pathlib import Path


DEBUG = True

# LOGGING
LOGS_DIR = "logs"
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "minimal": {"format": "%(message)s"},
        "detailed": {"format": "%(levelname)s %(asctime)s [%(name)s:%(filename)s:%(funcName)s:%(lineno)d]\n%(message)s\n"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "minimal",
            "level": logging.DEBUG,
        },
        "debug": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGS_DIR, "debug.log"),
            "maxBytes": 10485760,  # 1 MB
            "backupCount": 10,
            "formatter": "detailed",
            "level": logging.DEBUG,
        },
        "info": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGS_DIR, "info.log"),
            "maxBytes": 10485760,  # 1 MB
            "backupCount": 10,
            "formatter": "detailed",
            "level": logging.INFO,
        },
        "error": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": Path(LOGS_DIR, "error.log"),
            "maxBytes": 10485760,  # 1 MB
            "backupCount": 10,
            "formatter": "detailed",
            "level": logging.ERROR,
        },
    },
    "root": {
        "handlers": ["debug", "error"],
        "level": logging.DEBUG if DEBUG else logging.INFO,
        "propagate": True,
    },
}
logging_config.dictConfig(LOGGING_CONFIG)

# DRIVER
WEBDRIVER_PATH = "/home/ckr/.webdrivers_for_selenium/geckodriver"
HEADLESS = True
LOADING_TIMEOUT = 0.75
# SHOP_URL = "https://www.ozon.ru/seller/skyfors-301871/products/?miniapp=seller_301871"
SHOP_URL = "https://www.ozon.ru/brand/3q-25219578/category/elektronika-15500"

# PARSER

# SPREADSHEETS 
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
CREDS_PATH = "credentials.json"
SHEETS_API_VERSION = "v4"
SHEET_ID = "1_8CYhuQvkCVMJcBSD9EbkpNYPEr1VTdiOwSc2S45KdY"
