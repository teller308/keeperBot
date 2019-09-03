import logging

import gkeepapi
import keyring

from core import db
from models.gkeep_user import GKeepUser

logger = logging.getLogger(__name__)


class GKeepHandler:

    MASTER_TOKEN_NAME = 'google-keep-token'
    _instance = None

    @staticmethod
    def get_instance():
        if GKeepHandler._instance is None:
            return GKeepHandler()
        else:
            return GKeepHandler._instance

    def __init__(self) -> None:
        if self._instance is None:
            self._keep_instance = gkeepapi.Keep()
            self._active_user_emails = []

            GKeepHandler._instance = self

        else:
            raise Exception('This class is a singleton.')

    def _new_login(self, user_id: int, email: str, password: str) -> str:
        # try login in gkeep service
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('NEW GKEEP LOGIN TRY')
        self._keep_instance.login(email, password)

        # store token in keyring
        token = self._keep_instance.getMasterToken()
        keyring.set_password(self.MASTER_TOKEN_NAME, email, token)

        # to remember user
        new_user = GKeepUser(tg_user_id=user_id, email=email)
        db.session.add(new_user)
        db.session.commit()
        self._active_user_emails.append(email)

    def _resume_login(self, user_id: int, email: str) -> None:
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Try resume login for: {}'.format(email))
        token = keyring.get_password(self.MASTER_TOKEN_NAME, email)
        self._keep_instance.resume(email, token)
        self._active_user_emails.append(email)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Login resumed.')
        return token

    def log_in(self, user_id: int, email: str, password: str) -> str:
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('Handler got: {} {} {}'.format(
                user_id, email, password))
        try:
            if email in self._active_user_emails:
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug('ACTIVE USER')
                return 'User already in system.'
            elif GKeepUser.query.filter_by(email=email).first():
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug('REGISTERED USER')
                self._resume_login(user_id, email)
            else:
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug('NEW USER')
                self._new_login(user_id, email, password)
            return 'Success.'
        except Exception as exc:
            msg = 'Something went wrong when try to log in. {}'.format(exc)
            logger.error(msg)
            return 'Failed to log in.'

    def log_out(self):
        pass

    def create_note(self, name: str, content: str) -> None:
        self._keep_instance.createNote(name, content)
        self._keep_instance.sync()

    def read_note(self, name: str) -> str:
        pass

    def update_note(self) -> None:
        pass

    def delete_note(self) -> None:
        pass
