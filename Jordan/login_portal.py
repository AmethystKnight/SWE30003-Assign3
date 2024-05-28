from time import time
from constants import TKeys
from user_token import User_Token


class LoginPortal:
    """Logs in user and instantiates portal once it is finished processing
    via ACL inside Login"""
    def __init__(self, portal):
        self._user_name = None
        self._password = None
        self._has_logged = False
        self._p_ref = portal
        self._logins = [('admin', 'password'), ('foh', 'password'), ('boh', 'password')]

    def login(self) -> bool:
        from acl import ACL

        start_time = time()
        timeout_duration = 60 * 5

        while True:
            if time() - start_time > timeout_duration:
                print('timeout')
                return False
            user_name = input('username: ')
            password = input('password: ')
            for user, pwd in self._logins:
                if user == user_name and pwd == password:
                    token = User_Token(user_name, password)
                    acl = ACL()
                    acl.posses_token(token)
                    if acl.guide_token(self._p_ref):
                        return True
