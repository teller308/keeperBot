import json
import logging

import requests
import yaml
from flask import Flask, request

from utils.webhook_context_manager import WebhookContextManager


application = Flask(__name__)


# logging setup
with open('log_config.yaml') as log_config:
    log_config_dict = yaml.safe_load(log_config)
logging.config.dictConfig(log_config_dict)
logger = logging.getLogger(__name__)


# sensitive configuration data
with open('private/config.json') as private_config:
    config_dict = json.load(private_config)
config_dict['port'] = 443
config_dict['api_url'] = 'https://api.telegram.org/bot' + config_dict['token']


@application.route('/{}'.format(config_dict['token']), methods=['POST'])
def porcess_wh_response():
    # TODO move this paste of processing code to handler
    recieved_data = request.json
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug('MESSAGE_ID {}'.format(
            recieved_data['message']['message_id']))
        logger.debug('USERNAME {}'.format(
            recieved_data['message']['from']['username']))

    prepared_data = {}
    if 'text' in recieved_data['message']:
        prepared_data['chat_id'] = recieved_data['message']['chat']['id']
        prepared_data['text'] = 'I got: {}'.format(
            recieved_data['message']['text'])
        requests.post(url='{}/sendMessage'.format(config_dict['api_url']),
                      data=prepared_data)
    else:
        prepared_data['text'] = 'I got: {}'.format(recieved_data['message'])
        requests.post(url='{}/sendMessage'.format(config_dict['api_url']),
                      data=prepared_data)

    return 'New update recieved'


@application.route('/')
def process_all():
    WebhookContextManager.delete_webhook()
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug('MAIN PAGE REQUEST: {}'.format(request.text))
    return 'Hello from BOT'


if __name__ == '__main__':
    application.run(debug=True)
