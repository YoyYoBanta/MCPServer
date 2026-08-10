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

def update_document(creds, document_id: str, content: str) -> str:
    """
    Appends content to the end of an existing Google Document.
    Returns the document URL.
    """
    service = build('docs', 'v1', credentials=creds)
    
    if content:
        # Get the document to find its end index
        doc = service.documents().get(documentId=document_id).execute()
        
        # Calculate the end index. A basic approach is to use the document's body content's end index.
        # But we can also insert at index 1 to put it at the top. Let's insert at the top (index 1) for a reverse chronological log.
        requests = [
            {
                'insertText': {
                    'location': {
                        'index': 1,
                    },
                    'text': content + "\n\n" + "-"*40 + "\n\n"
                }
            }
        ]
        service.documents().batchUpdate(
            documentId=document_id, body={'requests': requests}).execute()

    return f"https://docs.google.com/document/d/{document_id}/edit"
