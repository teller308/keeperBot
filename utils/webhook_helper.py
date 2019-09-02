import logging

import requests

logger = logging.getLogger(__name__)


class WebhookHelper:
    def __init__(self, config) -> None:
        self._CERT_CHAIN = config['CERT']

        self._FQDN = config['FQDN']
        self._PORT = config['PORT']
        self._TOKEN = config['TOKEN']
        self._API_URL = 'https://api.telegram.org/bot' + self._TOKEN

    def set_webhook(self) -> dict:
        with open(self._CERT_CHAIN) as _CERTIFICATE:
            webhook_data = {'url': 'https://{}:{}/{}'.format(
                self._FQDN,
                self._PORT,
                self._TOKEN),
                'certificate': _CERTIFICATE, }

            print('Try POST webhook URL: {}'.format(
                self._API_URL + '/setWebhook'))
            resp = requests.post(url=self._API_URL + '/setWebhook',
                                 data=webhook_data,
                                 )
            return(resp.json())

    def get_webhook(self) -> dict:
        resp = requests.get(self._API_URL + '/getWebhookInfo')
        return(resp.json())

    def delete_webhook(self) -> dict:
        resp = requests.get(self._API_URL + '/deleteWebhook')
        return(resp.json())
