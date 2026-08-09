from googleapiclient.discovery import build

def create_document(creds, title: str, content: str) -> str:
    """
    Creates a new Google Document with the given title and content.
    Returns the document URL.
    """
    service = build('docs', 'v1', credentials=creds)
    
    # 1. Create the document
    body = {'title': title}
    doc = service.documents().create(body=body).execute()
    document_id = doc.get('documentId')
    
    # 2. Append the content
    if content:
        requests = [
            {
                'insertText': {
                    'location': {
                        'index': 1,
                    },
                    'text': content
                }
            }
        ]
        service.documents().batchUpdate(
            documentId=document_id, body={'requests': requests}).execute()

    return f"https://docs.google.com/document/d/{document_id}/edit"
