import base64
from email.message import EmailMessage
from googleapiclient.discovery import build

def draft_email(creds, to: list[str], subject: str, body: str) -> str:
    """
    Creates a draft email in Gmail.
    Returns the draft ID.
    """
    service = build('gmail', 'v1', credentials=creds)
    
    message = EmailMessage()
    message.set_content(body)
    message['To'] = ', '.join(to)
    message['Subject'] = subject
    
    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {
        'message': {
            'raw': encoded_message
        }
    }
    
    draft = service.users().drafts().create(userId="me", body=create_message).execute()
    return draft.get('id')
