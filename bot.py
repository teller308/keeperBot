import json
import logging

import requests
from flask import Flask, request

application = Flask(__name__)
logger = logging.getLogger(__name__)

# sensitive configuration data
if application.config.get('FQDN') is None:
    with open('private/config.json') as private_config:
        config_dict = json.load(private_config)
    application.config['FQDN'] = config_dict['fqdn']
    application.config['CERT'] = config_dict['cert']
    application.config['PORT'] = config_dict['port']
    application.config['TOKEN'] = config_dict['token']
    application.config['API_URL'] = 'https://api.telegram.org/bot' + \
        application.config['TOKEN']


@application.route('/{}'.format(application.config['TOKEN']), methods=['POST'])
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
        requests.post(url='{}/sendMessage'.format(
            application.config['API_URL']),
            data=prepared_data)
    else:
        prepared_data['text'] = 'I got: {}'.format(recieved_data['message'])
        requests.post(url='{}/sendMessage'.format(
            application.config['API_URL']),
            data=prepared_data)

    return 'New update recieved'


@application.route('/')
def process_all():
    return 'Hello.'


if __name__ == '__main__':
    application.run()
