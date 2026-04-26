from __future__ import print_function
import datetime
import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def main():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': 'Test Meet Link',
        'start': {
            'dateTime': '2025-08-01T10:00:00',
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': '2025-08-01T10:30:00',
            'timeZone': 'Asia/Kolkata',
        },
        'conferenceData': {
            'createRequest': {
                'requestId': 'unique-meet-123',
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                },
            },
        },
    }

    created_event = service.events().insert(calendarId='primary',
                                            body=event,
                                            conferenceDataVersion=1).execute()

    print("✅ Meet link:", created_event.get('hangoutLink'))

if __name__ == '__main__':
    main()
