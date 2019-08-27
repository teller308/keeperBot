import json
import logging

import requests


logger = logging.getLogger(__name__)


class WebhookContextManager:
    def __init__(self,
                 fqdn: str,
                 port: int,
                 token: str,
                 api_url: str) -> None:
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('fqdn {}, port {}', fqdn, port)

        self.fqdn = fqdn
        self.port = port
        self.token = token
        self.api_url = api_url

        self.methods_uri['set'] = '/setWebhook'
        self.methods_uri['delete'] = '/deleteWebhook'
        self.methods_uri['get_info'] = '/getWebhookInfo'

        with open('private/config.json') as config:
            config_dict = json.load(config)
            self._CERT_CHAIN = config_dict['CERT']

    def set_webhook(self) -> str:
        # TODO check if webhook already set - nothing to do
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
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug('set webhook response: {}'.format(resp.text))
            return(resp.text)

    def get_webhook(self) -> str:
        resp = requests.get(self.api_url + self.methods_uri['get_info'])
        self. logger.debug('get webhook response: {}'.format(resp.text))
        return(resp.text)

    def delete_webhook(self) -> str:
        resp = requests.get(self.api_url + self.methods_uri['delete'])
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('delete webhook response: {}'.format(resp.text))
        return(resp.text)
