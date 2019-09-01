class GKeepUser:

    # postgresql://user:password@hostname/database

    def __init__(self, user_id: int, email: str) -> None:
        # TODO check user_id and email uniqueness
        self._user_id = user_id
        self._email = email

    @property
    def user_id(self):
        return self._user_id

    @property
    def email(self):
        return self._email

    @user_id.setter
    def set_user_id(self, value):
        raise AttributeError

    @email.setter
    def set_email(self, value):
        raise AttributeError

    @id.getter
    def get_user_id(self):
        return self._user_id

    @email.getter
    def get_email(self):
        return self._email
