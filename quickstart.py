from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from download_attach import GetAttachments
from list_msg import *

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    user_id='me'
    results = service.users().labels().list(userId=user_id).execute()
    labels = results.get('labels', [])
    lab_ids = []
    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])
            if label['name'] == "UNREAD":
                lab_ids.append(label['id'])

    messages = ListMessagesWithLabels(service, user_id, label_ids=lab_ids)
    for msg in messages:
        pdp_msg = GetMessage(service, user_id, msg['id'])
        if pdp_msg:
            GetAttachments(service, user_id=user_id, msg_id=pdp_msg['id'])

if __name__ == '__main__':
    main()
