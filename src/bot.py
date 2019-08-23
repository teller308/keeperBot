import json

import requests
from flask import Flask, request

app = Flask(__name__)


with open('private/config.json') as config:
    config_dict = json.load(config)


_TOKEN = config_dict['TOKEN']
_FQDN = config_dict['FQDN']
_PORT = 8443
_SSL_CONTEXT = (config_dict['SSL_CONTEXT']['CERT'],
                config_dict['SSL_CONTEXT']['KEY'])
_CERT_FILE = _SSL_CONTEXT[0]

_API_URL = 'https://api.telegram.org/bot' + _TOKEN
_GET_UPDATES = '/getUpdates'

_SET_WEBHOOK = '/setWebhook'
_DELETE_WEBHOOK = '/deleteWebhook'
_GET_WEBHOOK_INFO = '/getWebhookInfo'


def setWebhook():
    resp = requests.get(_API_URL + _GET_WEBHOOK_INFO)
    print(resp.text)
    resp = requests.get(_API_URL + _DELETE_WEBHOOK)
    print(resp.text)

    with open(_CERT_FILE) as _CERTIFICATE:
        webhook_data = {'url': 'https://{}:{}/{}'.format(_FQDN, _PORT, _TOKEN),
                        'certificate': _CERTIFICATE, }

        print('Try POST webhook URL: {}'.format(_API_URL + _SET_WEBHOOK))
        resp = requests.post(url=_API_URL + _SET_WEBHOOK,
                             data=webhook_data,
                             verify=_CERT_FILE,
                             )
        print('Response: {}'.format(resp.text))


@app.route('/{}'.format(_TOKEN), methods=['POST'])
def porcess_wh_response():
    print(request.json)


@app.route('/')
def process_all():
    print('Hello')
    print(request.json)


if __name__ == '__main__':
    # setWebhook()

    app.run(host=_FQDN,
            port=_PORT,
            ssl_context=_SSL_CONTEXT,
            debug=True,)
