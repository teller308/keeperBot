import logging

import requests
from flask import request

from core import application
from utils.gkeep_handler import GKeepHandler
from utils.webhook_helper import WebhookHelper

logger = logging.getLogger(__name__)

# webhook setup
webhookHelper = WebhookHelper(application.config)
check_webhook_response = webhookHelper.get_webhook()
if check_webhook_response['result']['url'] == '':
    webhookHelper.set_webhook()

TOKEN = application.config['TOKEN']
API_URL = application.config['API_URL']

# handler setup
handler = GKeepHandler.get_instance()


@application.route('/{}'.format(application.config['TOKEN']), methods=['POST'])
def porcess_wh_response():
    recieved_data = request.json

    answer = handler.router(recieved_data)
    requests.post(
        url='{}/sendMessage'.format(API_URL), data=answer)
    return '200'


@application.route('/')
def process_all():
    return 'Hello.'


if __name__ == '__main__':
    application.run()
