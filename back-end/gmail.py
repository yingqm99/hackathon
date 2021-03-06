import pickle
import os.path
import json
from dateutil.parser import parse
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_messages(service, user_id):
    try:
        response = service.users().messages().list(userId=user_id, maxResults=100).execute()
        next_page = response["nextPageToken"]
        messages = [item.get('id') for item in response["messages"]]
        return messages
    except Exception as error:
        print('An error occurred: %s' % error)


def get_message(service, user_id, msg_ids):
    json_dict = []
    for msg_id in msg_ids:
        try:
            message = service.users().messages().get(userId=user_id, id=msg_id, format='metadata').execute()
            json_dict.append(message)
        except Exception as error:
            print('An error occurred: %s' % error) 
    return json_dict 


def clean_up(messages):
    json_dict = []
    oder = 0
    for msg in messages:
        df = {}
        df['id'] = msg['id']
        df['text'] = msg['snippet']
        headers = msg['payload']['headers']
        geojson = list(filter(lambda x: x['name'] == 'From',
                            headers))
        if geojson == []:
            print("no from", oder)
            continue
        df['sender'] = geojson[0].get('value')

        geojson = list(filter(lambda x: x['name'] == 'To',
                            headers))
        if geojson == []:
            print("no to", oder)
            continue
        df['receiver'] = geojson[0].get('value')

        geojson = list(filter(lambda x: x['name'] == 'Date',
                            headers))
        if geojson == []:
            print("no date", oder)
            continue

        date = parse(geojson[0].get('value'))
        df['date'] = str(date.year)+'{0:0=2d}'.format(date.month)+'{0:0=2d}'.format(date.day)
        json_dict.append(df)
        oder += 1
    return json_dict


def main():
    """Login with credentials.
    Request all messages.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'back-end/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    message_ids = get_messages(service, 'me')
    results = get_message(service, 'me', message_ids)
    textualize = clean_up(results)

    with open('texts.json', 'w') as json_file:
        json.dump(textualize, json_file)
    


if __name__ == '__main__':
    main()

