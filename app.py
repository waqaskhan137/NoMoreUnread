import os.path
import base64
from email import message_from_bytes
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']  # Need modify scope to mark as read

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def read_and_mark_unread_emails():
    service = get_gmail_service()
    next_page_token = None
    total_processed = 0

    while True:
        response = service.users().messages().list(
            userId='me',
            labelIds=['UNREAD'],
            maxResults=100,
            pageToken=next_page_token
        ).execute()

        messages = response.get('messages', [])
        if not messages:
            break

        for msg in messages:
            msg_id = msg['id']
            msg_data = service.users().messages().get(userId='me', id=msg_id).execute()
            payload = msg_data.get('payload', {})
            headers = payload.get('headers', [])

            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
            from_email = next((h['value'] for h in headers if h['name'] == 'From'), '(Unknown Sender)')

            body = ""
            parts = payload.get('parts', [])
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data')
                    if data:
                        body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
                        break

            print(f"From: {from_email}")
            print(f"Subject: {subject}")
            print(f"Body: {body[:200]}...")
            print("=" * 50)

            # ✅ Mark email as read
            service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()

            total_processed += 1

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    print(f"✅ Total unread emails read and marked as read: {total_processed}")

read_and_mark_unread_emails()
