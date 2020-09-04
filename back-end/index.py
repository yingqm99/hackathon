from flask import Flask

import json
import requests
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

app = Flask(__name__)

apikey = "LHiAsPDfojrabmyLdVSbw87gY4hVJScdoIyRD7nNHKao"
url = "https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/a624be02-9f6a-4a57-8b1c-2fa687021e3b/v3/tone"
version = "4.6.0"

authenticator = IAMAuthenticator( apikey )
tone_analyzer = ToneAnalyzerV3(
    version=version,
    authenticator=authenticator
)

tone_analyzer.set_service_url( url )


@app.route('/test')
def hello_world():

    text = 'Team, I know that times are tough! Product sales have been disappointing for the past three quarters. We have a competitive product, but we need to do a better job of selling it!'
    params = (('version', '2017-09-21'), ('text', text))
    response = requests.get(url, params=params, auth=('apikey', apikey))

    print(response)

    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
