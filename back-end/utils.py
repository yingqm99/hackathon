import json
import requests
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

APIKEY = "LHiAsPDfojrabmyLdVSbw87gY4hVJScdoIyRD7nNHKao"
URL = "https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/a624be02-9f6a-4a57-8b1c-2fa687021e3b"
VERSION = "4.6.0"

def bar_chart(data):
    return NotImplemented

def line_chart(data):
    return NotImplemented


def aggregate_by_date(data):
    """json_dict =
    {
        date_id:{
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
                    json_dict_temp[item['date']]['tones'][max_tone]['scores'] = max_score
                    json_dict_temp[item['date']]['tones'][max_tone]['count'] = 1
        else:
            json_dict_temp[item['date']] = {}
            json_dict_temp[item['date']]['count'] = 1
            if max_tone != '':
                json_dict_temp[item['date']]['tones'] = {}
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
    print(json_dict)


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
        item['document_tone'] = response['document_tone']
    aggregate_by_date(data)



if __name__ == '__main__':
    main()