from flask import Flask

import json
import requests
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

import pickle
import os.path
import json
import datetime
from dateutil.parser import parse
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from utils import aggregate_by_tone, aggregate_by_date, recent_tone, aggregate_by_person

app = Flask(__name__)

############### IBM ###############
apikey = "LHiAsPDfojrabmyLdVSbw87gY4hVJScdoIyRD7nNHKao" #TODO
url = "https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/a624be02-9f6a-4a57-8b1c-2fa687021e3b/v3/tone"
version = "4.6.0"

authenticator = IAMAuthenticator( apikey )
tone_analyzer = ToneAnalyzerV3(
    version=version,
    authenticator=authenticator
)

tone_analyzer.set_service_url( url )

################# GMAIL ################
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_messages(service, user_id):
    try:
        response = service.users().messages().list(userId=user_id, maxResults=50).execute()
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
            continue
        df['sender'] = geojson[0].get('value')

        geojson = list(filter(lambda x: x['name'] == 'To',
                            headers))
        if geojson == []:
            continue
        df['receiver'] = geojson[0].get('value')

        geojson = list(filter(lambda x: x['name'] == 'Date',
                            headers))
        if geojson == []:
            continue

        date = parse(geojson[0].get('value'))
        df['date'] = str(date.year)+'{0:0=2d}'.format(date.month)+'{0:0=2d}'.format(date.day)
        json_dict.append(df)
    return json_dict


def gmailAuth():
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
    print("textualize: ", textualize)
    return textualize


############# REST API ###############

@app.route('/test')
def hello_world():

    text = 'Team, I know that times are tough! Product sales have been disappointing for the past three quarters. We have a competitive product, but we need to do a better job of selling it!'
    response = requests.get(url, params=(('version', '2017-09-21'), ('text', text)), auth=('apikey', apikey))

    print(response)

    return 'Hello, World!'


@app.route('/recent_emotions')
def recent_emotion():
    with open('cache.json') as f:
        data = json.load(f)
    result = recent_tone(data)
    return result


@app.route('/personal_relations')
def personal_relations():
    with open('cache.json') as f:
        data = json.load(f)
    result = aggregate_by_person(data)
    return result


@app.route('/change_of_emotions')
def change_of_emotions():
    with open('cache.json') as f:
        data = json.load(f)
    result = aggregate_by_tone(data)
    print(result)
    list_json = []
    for item in result:
        if 'now' in result[item] and 'a_week_before' in result[item]:
            list_json.append({
                'tone_name': item,
                'change': result[item]['now']['score'] - result[item]['a_week_before']['score'],
                'most_recent_date': result[item]['most_recent_date']
            })
    return {
        'data': list_json
        }
    
@app.route('/emotion-calender')
def emotion_by_day():
    with open('cache.json') as f:
        data = json.load(f)
    result = aggregate_by_date(data)
    print(result)
    list_json = []
    for item in result:
        list_json.append({
            'date': item,
            'tone_name': result[item]['tone_name'],
            'tone_score': result[item]['tone_score']
        })
    return {
        'data': list_json
        }

@app.route('/email')
def extract_email():

    print("==========Receive the request from client side===============")
    emails = gmailAuth()
    # [{
    #   "id":"1745aec9cc4564f4",
    #   "text":"Your email preferences are currently set to a 4-hour Auto Digest, so you&#39;ll receive at most one email every 4 hours. You can customize your email preferences from your Account Settings page in the",
    #   "sender":"CF2020 on Piazza <no-reply@piazza.com>",
    #   "receiver":"duochen@umich.edu",
    #   "date":"Fri, 04 Sep 2020 21:01:23 +0000 (UTC)"
    # },...]
    print("==========Finished extracting emails===============")


    data = []
    for email in emails:
        emailid, text, date = email["id"], email["text"], email["date"]
        ### analyzing text
        toneRes = requests.get(url, params=(('version', '2017-09-21'), ('text', text)), auth=('apikey', apikey))
        toneRes = json.loads(toneRes.text)
        if "document_tone" not in toneRes:
            continue
        docTones = toneRes["document_tone"]["tones"]
        if not docTones:
            continue
        print("emailId:{}, Date:{}, docTones:{}".format(emailid, date, docTones))

        maxDocTone = max(docTones, key=lambda k : k['score'])

        data.append({
            'emailid': emailid,
            'date': date,
            'score': maxDocTone['score'],
            'tone': maxDocTone['tone_name']
        })

        email['document_tone'] = toneRes['document_tone']
    with open('cache-new.json', 'w') as json_file:
        json.dump(emails, json_file)

    return {
        'data': data,
        #deleted tones
    }


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
