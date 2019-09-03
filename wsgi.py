import logging
import logging.config

import yaml

from bot import application

# logging setup
with open('log_config.yaml') as log_config:
    log_config_dict = yaml.safe_load(log_config)
logging.config.dictConfig(log_config_dict)

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    application.run()
