import uuid
from constants import TKeys


class User_Token:
    def __init__(self, un, pa):
        self._user_name = un
        self._password = pa
        self._data = {TKeys.Username: self._user_name,
                      TKeys.Password: self._password}

    @property
    def data(self) -> dict:
        return self._data
