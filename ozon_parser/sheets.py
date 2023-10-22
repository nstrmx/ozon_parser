from typing import Optional, List
import os.path
import logging
import datetime as dt
from string import ascii_uppercase as abc
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from settings import CREDS_PATH, SCOPES, SHEETS_API_VERSION, SHEET_ID
from utils import hasmethod


log = logging.getLogger("default")


class GoogleService:
    creds_path = CREDS_PATH
    scopes = SCOPES

    def __init__(self):
        log.debug("Initializing GoogleService")
        self.creds = self.connect(self.creds_path, self.scopes)

    def connect(self, creds_path: str, scopes: List[str]) -> Optional[Credentials]:
        log.debug("Connecting to google service")
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            log.debug("Generating credentials from token.json")
            creds = Credentials.from_authorized_user_file('token.json', scopes)
        # If there are no (valid) credentials available, let the user log in.
        if creds == None or (hasattr(creds, "valid") and creds.valid == False):
            log.debug("Generating new credentials")
            if creds and creds.expired and creds.refresh_token:
                log.debug("Refreshing credentials")
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            log.debug("Saving credentials to token.json")
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds                                                            # type: ignore


class Sheet:
    google_class = GoogleService
    api_version = SHEETS_API_VERSION
    sheet_id = SHEET_ID

    def __init__(self):
        log.debug(f"Initializing sheets {self.api_version} with id={self.sheet_id}")
        google = self.google_class()
        service = build("sheets", self.api_version, credentials=google.creds)
        if not hasmethod(service, "spreadsheets"):
            raise Exception("Something went wrong while building sheets")
        self.sheets = service.spreadsheets()
        if not hasmethod(self.sheets, "values"):
            raise Exception("Something went wrong while building sheets")
        
    def get_range(self, sheet_range: str, dimension: str = "ROWS"):
        log.debug(f"Getting range {sheet_range} as {dimension}")
        response = (
            self.sheets
                .values()
                .get(spreadsheetId=self.sheet_id, range=f"{sheet_range}",
                     majorDimension=dimension)
                .execute()
        )
        log.debug(response)
        return response

    def batch_update(self, sheet_range: str, values: List[List[str]]):
        log.debug(f"Updating range {sheet_range}")
        data = [{"values": values, "range": f"{sheet_range}"}]
        body = {"valueInputOption": "USER_ENTERED", "data": data}
        response = (
            self.sheets
                .values()
                .batchUpdate(spreadsheetId=self.sheet_id, body=body)
                .execute()
        )
        log.debug(response)
        return response

    def clear_range(self, sheet_range):
        log.debug(f"Clearing range {sheet_range}")
        response = (
            self.sheets
                .values()
                .clear(spreadsheetId=self.sheet_id, range=sheet_range, body={})
                .execute()
        )
        log.debug(response)
        return response

    def generate(self, rows_itr):
        table = []
        for i, item in enumerate(rows_itr):
            # Formatting data for google sheets
            log.debug(item)
            row = [str(i), *item.get_values(), str(dt.datetime.now())]
            table.append(row)
            yield item
        if len(table) == 0:
            log.debug("Nothing to save. Closing.")
            return
        self.clear_range("Лист1!A2:Z")
        number_of_columns = len(max(table, key=lambda row: len(row)))
        number_of_rows = len(table)
        sheet_range = f"Лист1!A2:{abc[number_of_columns]}{number_of_rows + 2}"
        self.batch_update(sheet_range, table)
        self.get_range(sheet_range)
