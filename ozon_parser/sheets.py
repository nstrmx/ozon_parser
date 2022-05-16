from typing import Any, Optional, List

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils import hasmethod, log



def response_wrapper(func):
    def wrapper(*args, **kwargs) -> Optional[Any]:
        try:
            return func(*args, **kwargs)
        except HttpError as http_error:
            print(http_error)
    return wrapper




class Sheet:
    def __init__(self, sheets: Any, sheet_id):
        log("Initializing Sheet")

        self.sheet_id = sheet_id
        if hasmethod(sheets, "values"):
            self.values = sheets.values
        else:
            raise Exception("Invalid 'sheets' parameter. Sheets must have 'values' method.")

    @response_wrapper
    def get_range(self, sheet_range: str, dimension: str = "ROWS"):
        log(f"Getting data in range {sheet_range} as {dimension}")

        return self.values().get(
            spreadsheetId = self.sheet_id,
            range = f"{sheet_range}",
            majorDimension = dimension
        ).execute()

    @response_wrapper
    def batch_update(self, sheet_range: str, values: List[List[str]]):
        log(f"Updating data in range {sheet_range}")

        data = [{"values": values, "range": f"{sheet_range}"}]
        body = {"valueInputOption": "USER_ENTERED", "data": data}
        return self.values().batchUpdate(spreadsheetId=self.sheet_id, body=body).execute()




class GoogleService:
    def __init__(self, creds_path: str, scopes: List[str]):
        log("Initializing GoogleService")

        self.creds = self.connect(creds_path, scopes)

    def connect(self, creds_path: str, scopes: List[str]) -> Optional[Credentials]:
        log("Connecting to google service")

        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            log("Generating credentials from token.json")
            creds = Credentials.from_authorized_user_file('token.json', scopes)

        # If there are no (valid) credentials available, let the user log in.
        if creds == None or creds.valid == False:
            log("Generating new credentials")

            if creds and creds.expired and creds.refresh_token:
                log("Refreshing credentials")

                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, scopes)
                creds = flow.run_local_server(port=0)
            
            # Save the credentials for the next run
            log("Saving credentials to token.json")

            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return creds

    def build_sheets(self, api_version, sheet_id, *args, **kwargs) -> Sheet:
        log(f"Building sheets {api_version} with id={sheet_id}")

        service = build("sheets", api_version, *args, credentials=self.creds, **kwargs)

        if hasmethod(service, "spreadsheets"):
            return Sheet(service.spreadsheets(), sheet_id)




def main():
    pass




if __name__ == "__main__":
    main()