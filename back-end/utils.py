import datetime
import json
import re

import requests
from dateutil.parser import parse
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ToneAnalyzerV3

APIKEY = "" #TODO
URL = "" #TODO
VERSION = "4.6.0"
MY_EMAIL = "zhuhongt@umich.edu"
NEGATIVE = ['Anger','Fear','Sadness']
POSITIVE = ['Joy', 'Confidence']

def aggregate_by_person(data):
    list_contacts = {}
    for item in data:
        if MY_EMAIL in item['receiver'].lower():#TODO
            text = re.sub(r"<.*>", " ", item['sender'].lower())
            print(text)
            if text not in list_contacts: 
                list_contacts[text] = {}
            tones = item['document_tone']['tones']
            if not tones:
                continue
            this_tone = max(tones, key=lambda k : k['score'])
            this_tone = this_tone['tone_name']
            if this_tone in list_contacts[text]:
                list_contacts[text][this_tone] += 1
            else:
                list_contacts[text][this_tone] = 1
    list_json = []
    for contact in list_contacts:
        overall_score = 0
        for tones in list_contacts[contact]:
            if tones in NEGATIVE:
                overall_score -= list_contacts[contact][tones]
            if tones in POSITIVE:
                overall_score += list_contacts[contact][tones]
        list_json.append({
            "person_name": contact,
            "score": overall_score
        })
    return {
        "data": list_json
    }


def recent_tone(data):
    """json_dict =
    {
        "tone_name" : str,
        "count" : int,
    }
    """
    json_dict = {}
    for item in data:
        tones = item['document_tone']['tones']
        for tone in tones:
            if tone['tone_name'] == '':
                continue
            if tone['tone_name'] in json_dict:
                json_dict[tone['tone_name']] += 1
            else:
                json_dict[tone['tone_name']] = 1
    list_json = []
    for key in json_dict:
        list_json.append({
            "tone_name": key,
            "count": json_dict[key]
        })
    return {
        'data': list_json
    }


def aggregate_by_tone(data):
    """json_dict =
    {
        emotion_name:{
            "now": {
                "score": float,
                "count": int,
            },
            "a_week_before": {
                "score": float,
                "count": int,
            },
            "most_recent_date": int,
        }
    }
    """
    now = datetime.date.today()
    date_one = str(now.year)+'{0:0=2d}'.format(now.month)+'{0:0=2d}'.format(now.day)
    one_week_ago = now - datetime.timedelta(days=2) #TODO:change days
    date_two = str(one_week_ago.year)+'{0:0=2d}'.format(one_week_ago.month)+'{0:0=2d}'.format(one_week_ago.day)
    two_week_ago = now - datetime.timedelta(days=5) #TODO:change days
    date_three = str(two_week_ago.year)+'{0:0=2d}'.format(two_week_ago.month)+'{0:0=2d}'.format(two_week_ago.day)
    recent_json_dict = {}
    previous_json_dict = {}
    most_recent = {}
    for item in data:

        if 'document_tone' not in item:
            continue

        tones = item['document_tone']['tones']

        if int(item['date']) > int(date_two):
            for tone in tones:
                if tone['tone_name'] == '':
                    continue
                if tone['tone_name'] in recent_json_dict:
                    recent_json_dict[tone['tone_name']]["score"] += tone['score']
                    recent_json_dict[tone['tone_name']]["count"] += 1
                else:
                    recent_json_dict[tone['tone_name']] = {}
                    recent_json_dict[tone['tone_name']]["score"] = tone['score']
                    recent_json_dict[tone['tone_name']]["count"] = 1
                if tone['tone_name'] not in most_recent:
                    most_recent[tone['tone_name']] = item['date']
                elif tone['tone_name'] > most_recent[tone['tone_name']]:
                    most_recent[tone['tone_name']] = item['date']
        elif int(item['date']) > int(date_three):
            for tone in tones:
                if tone['tone_name'] == '':
                    continue
                if tone['tone_name'] in previous_json_dict:
                    previous_json_dict[tone['tone_name']]['score'] += tone['score']
                    previous_json_dict[tone['tone_name']]['count'] += 1
                else:
                    previous_json_dict[tone['tone_name']] = {}
                    previous_json_dict[tone['tone_name']]['score'] = tone['score']
                    previous_json_dict[tone['tone_name']]['count'] = 1

                if tone['tone_name'] not in most_recent:
                    most_recent[tone['tone_name']] = item['date']
                elif item['date'] > most_recent[tone['tone_name']]:
                    most_recent[tone['tone_name']] = item['date']
    json_dict = {}
    for tone in previous_json_dict:
        json_dict[tone] = {}
        json_dict[tone]['a_week_before'] = {}
        json_dict[tone]['a_week_before']['score'] = previous_json_dict[tone]['score'] / previous_json_dict[tone]['count']
        json_dict[tone]['a_week_before']['count'] = previous_json_dict[tone]['count']
        json_dict[tone]['most_recent_date'] = most_recent[tone]

    for tone in recent_json_dict:
        if tone not in json_dict:
            json_dict[tone] = {}
        json_dict[tone]['now'] = {}
        json_dict[tone]['now']['score'] = recent_json_dict[tone]['score'] / recent_json_dict[tone]['count']
        json_dict[tone]['now']['count'] = recent_json_dict[tone]['count']
        json_dict[tone]['most_recent_date'] = most_recent[tone]

    print(json_dict)
    return json_dict


def aggregate_by_date(data):
    """json_dict =
    {
        date:{
            'count': int,
            'tone_name': str,
            'tone_score': float,
        }
    }
    """
    json_dict_temp = {}
    for item in data:
        tones = item['document_tone']['tones']
        max_score = 0
        max_tone = ''
        for tone in tones:
            if max_score <= tone['score']:
                max_score = tone['score']
                max_tone = tone['tone_name']

        if item['date'] in json_dict_temp:
            json_dict_temp[item['date']]['count'] += 1
            if max_tone != '':
                if max_tone in json_dict_temp[item['date']]['tones']:
                    json_dict_temp[item['date']]['tones'][max_tone]['scores'] += max_score
                    json_dict_temp[item['date']]['tones'][max_tone]['count'] += 1
                else:
                    json_dict_temp[item['date']]['tones'][max_tone] = {}
                    json_dict_temp[item['date']]['tones'][max_tone]['scores'] = max_score
                    json_dict_temp[item['date']]['tones'][max_tone]['count'] = 1
        else:
            json_dict_temp[item['date']] = {}
            json_dict_temp[item['date']]['count'] = 1
            json_dict_temp[item['date']]['tones'] = {}
            if max_tone != '':
                json_dict_temp[item['date']]['tones'][max_tone] = {}
                json_dict_temp[item['date']]['tones'][max_tone]['scores'] = max_score
                json_dict_temp[item['date']]['tones'][max_tone]['count'] = 1
        json_dict = {}
        for item in json_dict_temp:
            json_dict[item] = {}
            json_dict[item]['count'] = json_dict_temp[item]['count']
            max_tone = ''
            max_score = 0
            if 'tones' in json_dict_temp[item]:
                for tone in json_dict_temp[item]['tones']:
                    score = json_dict_temp[item]['tones'][tone]['scores']/json_dict_temp[item]['tones'][tone]['count']
                    if max_score <= score:
                        max_score = score
                        max_tone = tone
            json_dict[item]['tone_name'] = max_tone
            json_dict[item]['tone_score'] = max_score
    return json_dict


def main():
    with open('texts.json') as f:
        data = json.load(f)

    authenticator = IAMAuthenticator( APIKEY )
    tone_analyzer = ToneAnalyzerV3(
        version=VERSION,
        authenticator=authenticator
    )

    tone_analyzer.set_service_url( URL )
    for item in data:
        params = (
            ('version', '2017-09-21'),
            ('text', item['text']),
        )

        response = requests.get(URL+'/v3/tone', params=params, auth=('apikey', APIKEY))
        response = json.loads(response.text)
        print(response)
        
        if 'document_tone' not in response:
            break

        item['document_tone'] = response['document_tone']

    with open('back-end/cache-new.json', 'w') as json_file:
        json.dump(data, json_file)

    #print(aggregate_by_tone(data))


if __name__ == '__main__':
    main()
