import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/gmail.compose'
]

def authenticate():
    """
    Authenticates the user with Google APIs using OAuth2.
    Returns the Credentials object.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    token_path = os.environ.get('TOKEN_PATH', 'token.json')
    creds_path = os.environ.get('CREDENTIALS_PATH', 'credentials.json')

    # --- Railway Base64 Injection ---
    import base64
    if os.environ.get('GOOGLE_TOKEN_B64'):
        try:
            with open(token_path, 'wb') as f:
                f.write(base64.b64decode(os.environ['GOOGLE_TOKEN_B64']))
        except Exception as e:
            print(f"Failed to decode GOOGLE_TOKEN_B64: {e}")

    if os.environ.get('GOOGLE_CREDENTIALS_B64'):
        try:
            with open(creds_path, 'wb') as f:
                f.write(base64.b64decode(os.environ['GOOGLE_CREDENTIALS_B64']))
        except Exception as e:
            print(f"Failed to decode GOOGLE_CREDENTIALS_B64: {e}")
    # --------------------------------

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                raise FileNotFoundError(
                    f"Missing '{creds_path}'. Please download your desktop client "
                    "OAuth credentials from Google Cloud Console and save it at this path."
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
            
    return creds
