import logging

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


@application.route('/{}'.format(application.config['TOKEN']), methods=['POST'])
def porcess_wh_response():
    try:
        handler = GKeepHandler.get_instance()
        recieved_data = request.json
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('FULL JSON RESPONCE {}'.format(recieved_data))

        if recieved_data.get('message') is not None:
            entities = recieved_data['message'].get('entities')
            if entities is not None:
                entity_type = entities[0].get('type')
                if entity_type == 'bot_command':
                    user_id = recieved_data['message']['from']['id']
                    credentials = recieved_data['message']['text'].split(' ')
                    if len(credentials) < 3:
                        logger.error('Wrong arguments.')
                        return 'Wrong arguments.'
                    email = credentials[1]
                    pwd = credentials[2]
                    handler.log_in(user_id, email, pwd)
    except Exception as exc:
        msg = 'Something went wrong in webhook processing {}'.format(exc)
        logger.error(msg)
    finally:
        # TODO remove dev mode update skipping
        return 'Proceed pls. We do not need update duplication now.'


@application.route('/')
def process_all():
    return 'Hello.'


if __name__ == '__main__':
    application.run()
