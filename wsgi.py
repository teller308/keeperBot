import logging

from bot import application, config_dict
from utils.webhook_context_manager import WebhookContextManager


logger = logging.getLogger(__name__)


if __name__ == '__main__':
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug('before run')
    with WebhookContextManager(**config_dict):
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('in whcm')
        application.run(debug=True)
