import logging
from functools import wraps

import gkeepapi
import keyring

logger = logging.getLogger(__name__)


class GKeepHandler():

    MASTER_TOKEN_NAME = 'google-keep-token'

    def __init__(self) -> None:
        self.keep_instance = gkeepapi.Keep()
        self.authorized_users = []  # List of active Users

    def log_in(self, user_id: int, email: str, password: str) -> str:
        self.keep_instance.login(email, password)
        token = self.keep_instance.getMasterToken()
        keyring.set_password(self.MASTER_TOKEN_NAME, email, token)
        # new_user = GKeepUser(id, email)
        self.authorized_users.append(user_id)

    def resume_login(self, email: str) -> None:
        token = self.keyring_search(email)
        self.keep_instance.resume(email, token)

    def keyring_search(self, email: str) -> str:
        token = keyring.get_password(self.MASTER_TOKEN_NAME, email)
        return token

    def check_logged_in(self, func, user_id) -> object:
        @wraps(func, user_id)
        def wrapper(*args, **kwargs):
            if user_id in self.authorized_users:
                return func(*args, **kwargs)
            return 'You are not logged in.'
        return wrapper

    @check_logged_in
    def create(self, name: str, content: str) -> None:
        self.keep_instance.createNote(name, content)
        self.keep_instance.sync()

    @check_logged_in
    def read(self, name: str) -> str:
        pass

    @check_logged_in
    def update(self) -> None:
        pass

    @check_logged_in
    def delete(self) -> None:
        pass
