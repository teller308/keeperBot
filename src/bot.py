import json

import requests
from flask import Flask

app = Flask(__name__)


with open('config.json') as config:
    json_dict = json.load(config)


_TOKEN = json_dict['token']
_BASE_URL = 'https://api.telegram.org/bot' + _TOKEN
_METHOD = '/getUpdates'

with open('result.json', 'w') as jfile:
    json_resp = requests.get(_BASE_URL + _METHOD)
    json.dump(json_resp.json(), jfile)


if __name__ == '__main__':
    app.run(debug=True)
