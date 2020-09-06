
apikey = ""
url = "https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/a624be02-9f6a-4a57-8b1c-2fa687021e3b"
version = "4.6.0"

import json
import requests
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator( apikey )
tone_analyzer = ToneAnalyzerV3(
    version=version,
    authenticator=authenticator
)

tone_analyzer.set_service_url( url )

# curl -X GET -u "apikey:drrjUkHl_QBYeLBMQZdsJpab32YkSIZkEmnbhU8VDgqe" \
# "https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/1abc1b3d-1aba-4341-8085-098e63618c83/v3/tone?version=2017-09-21&text=Team%2C%20I%20know%20that%20times%20are%20tough%21%20Product%20sales%20have%20been%20disappointing%20for%20the%20past%20three%20quarters.%20We%20have%20a%20competitive%20product%2C%20but%20we%20need%20to%20do%20a%20better%20job%20of%20selling%20it%21"

text = 'Team, I know that times are tough! Product sales have been disappointing for the past three quarters. We have a competitive product, but we need to do a better job of selling it!'

params = (
    ('version', '2017-09-21'),
    ('text', text),
)

response = requests.get('https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/a624be02-9f6a-4a57-8b1c-2fa687021e3b/v3/tone', params=params, auth=('apikey', ''))


print(response.text)

# {
#    "document_tone":{
#       "tones":[
#          {
#             "score":0.6165,
#             "tone_id":"sadness",
#             "tone_name":"Sadness"
#          },
#          {
#             "score":0.829888,
#             "tone_id":"analytical",
#             "tone_name":"Analytical"
#          }
#       ]
#    },
#    "sentences_tone":[
#       {
#          "sentence_id":0,
#          "text":"Team, I know that times are tough!",
#          "tones":[
#             {
#                "score":0.801827,
#                "tone_id":"analytical",
#                "tone_name":"Analytical"
#             }
#          ]
#       },
#       {
#          "sentence_id":1,
#          "text":"Product sales have been disappointing for the past three quarters.",
#          "tones":[
#             {
#                "score":0.771241,
#                "tone_id":"sadness",
#                "tone_name":"Sadness"
#             },
#             {
#                "score":0.687768,
#                "tone_id":"analytical",
#                "tone_name":"Analytical"
#             }
#          ]
#       },
#       {
#          "sentence_id":2,
#          "text":"We have a competitive product, but we need to do a better job of selling it!",
#          "tones":[
#             {
#                "score":0.506763,
#                "tone_id":"analytical",
#                "tone_name":"Analytical"
#             }
#          ]
#       }
#    ]
# }