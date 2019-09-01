import json
import logging

import requests


logger = logging.getLogger(__name__)


class WebhookHelper:
    def __init__(self,
                 fqdn: str,
                 port: int,
                 token: str,
                 api_url: str
                 ) -> None:
        self.fqdn = fqdn
        self.port = port
        self.token = token
        self.api_url = api_url

        self.methods_uri = {}
        self.methods_uri['set'] = '/setWebhook'
        self.methods_uri['delete'] = '/deleteWebhook'
        self.methods_uri['get_info'] = '/getWebhookInfo'

        with open('private/config.json') as config:
            config_dict = json.load(config)
            self._CERT_CHAIN = config_dict['cert']

    def set_webhook(self) -> dict:
        with open(self._CERT_CHAIN) as _CERTIFICATE:
            webhook_data = {'url': 'https://{}:{}/{}'.format(
                self.fqdn,
                self.port,
                self.token),
                'certificate': _CERTIFICATE, }

            print('Try POST webhook URL: {}'.format(
                self.api_url + self.methods_uri['set']))
            resp = requests.post(url=self.api_url + self.methods_uri['set'],
                                 data=webhook_data,
                                 )
            return(resp.json())

    def get_webhook(self) -> dict:
        resp = requests.get(self.api_url + self.methods_uri['get_info'])
        return(resp.json())

    def delete_webhook(self) -> dict:
        resp = requests.get(self.api_url + self.methods_uri['delete'])
        return(resp.json())
