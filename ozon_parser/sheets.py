import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", 
          "https://www.googleapis.com/auth/drive"]

CREDS_PATH = "client_secret_455291594172-kfjqu8f362vbgr2bq9mq50b401nr88cl.apps.googleusercontent.com.json"
SHEET_ID = "1_8CYhuQvkCVMJcBSD9EbkpNYPEr1VTdiOwSc2S45KdY"

def connect():
    creds = None
    
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def response_wrapper(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HttpError as http_error:
            print(http_error)
    return wrapper

@response_wrapper
def get_range(sheet, list_id, range, dim="ROWS"):
    return sheet.values().get(
        spreadsheetId = SHEET_ID,
        range = f"{list_id}!{range}",
        majorDimension = dim
    ).execute()

@response_wrapper
def batch_update(sheet, list_id, range, values):
    data = [{"values": values, "range": f"{list_id}!{range}"}]
    body = {"valueInputOption": "USER_ENTERED", "data": data}
    return sheet.values().batchUpdate(spreadsheetId=SHEET_ID, body=body).execute()