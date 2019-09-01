class GKeepUser:

    # postgresql://user:password@hostname/database

    def __init__(self, id: int, email: str) -> None:
        # TODO check id and email uniqueness
        self._id = id
        self._email = email

    @property
    def id(self):
        return self._id

    @property
    def email(self):
        return self._email

    @id.setter
    def set_id(self, value):
        raise AttributeError

    @email.setter
    def set_email(self, value):
        raise AttributeError

    @id.getter
    def get_id(self):
        return self._id

    @email.getter
    def get_email(self):
        return self._email
