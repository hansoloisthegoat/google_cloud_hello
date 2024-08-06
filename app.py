import streamlit as st
import os.path
import base64
import json
import re
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
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
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

def list_messages(service, user_id):
    results = service.users().messages().list(userId=user_id).execute()
    messages = results.get('messages', [])
    return messages

def get_message(service, msg_id, user_id):
    message = service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
    return message

def get_email_content(message):
    payload = message['payload']
    headers = payload.get('headers')
    parts = payload.get('parts')
    
    subject = ''
    from_email = ''
    body = ''
    
    if headers:
        for header in headers:
            if header.get('name') == 'Subject':
                subject = header.get('value')
            if header.get('name') == 'From':
                from_email = header.get('value')

    if parts:
        for part in parts:
            if part['mimeType'] == 'text/plain':
                body = base64.urlsafe_b64decode(part['body']['data'].encode('ASCII')).decode('utf-8')
                break
    
    return subject, from_email, body

def main():
    st.title('Gmail Inbox Reader')

    user_email = st.text_input('Enter the email address of the inbox you want to read from:', 'me')
    
    if st.button('Fetch Emails'):
        service = get_gmail_service()
        messages = list_messages(service, user_email)
        
        if messages:
            for msg in messages[:10]:  # Displaying only the first 10 messages for simplicity
                message = get_message(service, msg['id'], user_email)
                subject, from_email, body = get_email_content(message)
                
                st.subheader(f'Subject: {subject}')
                st.write(f'From: {from_email}')
                st.write(f'Body: {body}')
                st.write('---')

if __name__ == '__main__':
    main()

