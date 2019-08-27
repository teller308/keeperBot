import logging

from bot import application


logger = logging.getLogger(__name__)


if __name__ == '__main__':
    application.run(debug=True)
