import logging
from bot import application


if __name__ == '__main__':

    # setup flask and gunicorn logs
    gunicorn_logger = logging.getLogger('gunicorn.error')
    application.logger.handlers = gunicorn_logger.handlers
    application.logger.setLevel(gunicorn_logger.level)

    application.run()
