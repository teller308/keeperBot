import json
import logging
import logging.config

import yaml

from bot import application
from utils.webhook_helper import WebhookHelper

# logging setup
with open('log_config.yaml') as log_config:
    log_config_dict = yaml.safe_load(log_config)
logging.config.dictConfig(log_config_dict)

logger = logging.getLogger(__name__)

# webhook setup
webhookHelper = WebhookHelper(application.config)
check_webhook_response = webhookHelper.get_webhook()
if check_webhook_response['result']['url'] == '':
    webhookHelper.set_webhook()

# SQLAlchemy setup
with open('private/config.json') as private_config:
    config_dict = json.load(private_config)
DB_URL = 'postgresql://{user}:{pass}@{host}/{database}'.format_map(
    config_dict['db'])
application.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


if __name__ == '__main__':
    application.run()
