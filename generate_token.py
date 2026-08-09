from dotenv import load_dotenv
import os
from google_auth_oauthlib.flow import InstalledAppFlow

load_dotenv()
creds_path = os.environ.get('CREDENTIALS_PATH', 'credentials.json')
token_path = os.environ.get('TOKEN_PATH', 'token.json')
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/gmail.compose'
]
flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
creds = flow.run_local_server(port=0, open_browser=False)
with open(token_path, 'w') as token:
    token.write(creds.to_json())
print("Token saved successfully!")
