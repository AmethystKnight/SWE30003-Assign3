from Inherit_Module import ITokenGuide
from enum import Enum
from Portal import *
from time import time


class TKeys(Enum):
    Username = 0,
    Password = 1,
    Privilege = 2,
    PortalKey = 3


class User_Token:
    def __init__(self, un, pa):
        self._user_name = un
        self._password = pa
        self._data = {TKeys.Username.value: self._user_name, TKeys.Password.value: self._password}

    @property
    def data(self) -> dict:
        # Return a copy of the dictionary to prevent modification
        return self._data.copy()


class LoginPortal:
    def __init__(self, portal: Portal):
        self._user_name = None
        self._password = None
        self._has_logged = False  # UI could use this for account switching flag
        self._p_ref = portal
        self._logins = [('admin', 'password')
            , ('foh', 'password')
            , ('boh', 'password')]

    def Login(self) -> bool:
        start_time = time()  # Record the start time
        timeout_duration = 60 * 5  # 5 minutes timeout

        while True:
            if time() - start_time > timeout_duration:
                print('timeout')
                return False
            user_name = input('username: ')
            password = input('password: ')
            for user, pwd in self._logins:
                if user == user_name and pwd == password:
                    token = User_Token(user_name, password)
                    # acl responsible for pushing token
                    acl = ACL()
                    acl.PossesToken(token)
                    acl.GuideToken(self._p_ref)
                    return True


class ACL(ITokenGuide):
    _privileges = {'admin': 1, 'foh': 0, 'boh': 0}
    _portals = {'admin': BusinessPortal, 'foh': FOHPortal, 'boh': BOHPortal}
    _token = None

    def PossesToken(self, user: User_Token):
        _token = user
        user_name = user.data[TKeys.Username]
        user.data.update({TKeys.Privilege: self._privileges[user_name]})
        user.data.update({TKeys.PortalKey: self._portals[user_name]})

    def GuideToken(self, next_guide: ITokenGuide):
        next_guide.GuideToken(self._token)
