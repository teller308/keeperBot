import json

import requests
from flask import Flask, request


app = Flask(__name__)


with open('private/config.json') as config:
    json_dict = json.load(config)


_TOKEN = json_dict['token']
_DOMAIN = json_dict['domain']

_BASE_URL = 'https://api.telegram.org/bot' + _TOKEN

_GET_UPDATES = '/getUpdates'

_SET_WEBHOOK = '/setWebhook'
_DELETE_WEBHOOK = '/deleteWebhook'
_GET_WEBHOOK_INFO = '/getWebhookInfo'

_ALLOWED_WEBHOOK = '/webhook' + _TOKEN


def setWebhook():
    with open('private/keeper_wh_public.pem') as certfile:
        resp = requests.get(_BASE_URL + _GET_WEBHOOK_INFO)
        print(resp.text)
        resp = requests.get(_BASE_URL + _DELETE_WEBHOOK)
        print(resp.text)

        webhook_data = {'url': _DOMAIN + _ALLOWED_WEBHOOK,
                        'certificate': certfile, }
        print('try to get the: ' + _BASE_URL + _SET_WEBHOOK)
        resp = requests.post(_BASE_URL + _SET_WEBHOOK, data=webhook_data)
        print(resp.text)


@app.route(_ALLOWED_WEBHOOK, methods=['POST'])
def porcess_wh_response():
    print(request.json)


@app.route('/', methods=['GET', 'POST'])
def process_all():
    print(request.json)


if __name__ == '__main__':
    setWebhook()
    app.run(debug=True, port=8443)
