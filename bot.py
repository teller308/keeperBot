import json

import requests
from flask import Flask, request

application = Flask(__name__)


with open('private/config.json') as config:
    config_dict = json.load(config)


_TOKEN = config_dict['TOKEN']
_FQDN = config_dict['FQDN']
_PORT = 443
_CERT_CHAIN = config_dict['SSL_CONTEXT']['CERT']

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

    with open(_CERT_CHAIN) as _CERTIFICATE:
        webhook_data = {'url': 'https://{}:{}/{}'.format(_FQDN, _PORT, _TOKEN),
                        'certificate': _CERTIFICATE, }

        print('Try POST webhook URL: {}'.format(
            _API_URL + _SET_WEBHOOK))
        resp = requests.post(url=_API_URL + _SET_WEBHOOK,
                             data=webhook_data,
                             # verify=_CERT_KEY,
                             # verify=True,
                             )
        print('Response: {}'.format(resp.text))


@application.route('/{}'.format(_TOKEN), methods=['POST'])
def porcess_wh_response():
    recieved_data = request.json
    print('request.json: ', str(recieved_data))
    prepared_data = {}
    prepared_data['chat_id'] = recieved_data['message']['chat']['id']
    prepared_data['text'] = 'I got: {}'.format(
        recieved_data['message']['text'])
    requests.post(url='{}/sendMessage'.format(_API_URL), data=prepared_data)

    return 'New update recieved'


@application.route('/')
def process_all():
    # setWebhook()
    print('request.json: ', str(request.json))
    return 'Hello from BOT'


if __name__ == '__main__':
    application.run(debug=True)
