import uuid
from Inherit_Module import Singleton, ITokenGuide, Portal, BusinessPortal, BOHPortal, FOHPortal, TKeys
from enum import Enum
from Portal import *
from time import time


class User_Token:
    def __init__(self, un, pa):
        self._user_name = un
        self._password = pa
        self._data = {TKeys.Username: self._user_name,
                      TKeys.Password: self._password}

    @property
    def data(self) -> dict:
        # Return a copy of the dictionary to prevent modification
        return self._data


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
                    if acl.GuideToken(self._p_ref):
                        return True

                    # return True


class ACL(ITokenGuide):

    def __init__(self):
        self._privileges = {'admin': 1, 'foh': 0, 'boh': 0}
        self._portals = {'admin': BusinessPortal, 'foh': FOHPortal, 'boh': BOHPortal}
        self._token = None

    def PossesToken(self, user: User_Token):
        if self._token is not None:
            print("ACL queue")
        self._token = user
        if TKeys.PortalKey not in user.data or TKeys.Privilege not in user.data:
            print("adding data via acl")
            user_name = self._token.data[TKeys.Username]
            self._token.data.update({TKeys.Privilege: self._privileges[user_name]})
            self._token.data.update({TKeys.PortalKey: self._portals[user_name]})
            print(self._token.data)

    def GuideToken(self, next_guide: ITokenGuide) -> bool:
        privilege = self._token.data.get(TKeys.Privilege, -1)  # Default to 0 if not found
        if privilege < next_guide.AccessLevel():
            print("You do not have access")
            return False
        else:
            next_guide.PossesToken(self._token)
            return True

        # if self._token.data[TKeys.Privilege] <= next_guide.AccessLevel():
        #     print("You do not have access")
        # else:
        #     next_guide.PossesToken(self._token)
        #     self._token = None

    def AccessLevel(self) -> int:
        return 0


class Session(Singleton):
    from multiprocessing import Process
    """Session uses mac as an id, because it would be unique inside your network,
    this is not intended for a global program but one that is run locally and does not want to double up
    on logins on the same device"""

    def __init__(self):
        super(Session, self).__init__()
        self.sessions = {}
        self.acl = ACL()

    def New_Session(self):
        """The idea is to hide the mac in the meta deta as much as possible"""
        mac = hex(uuid.getnode())
        if mac in self.sessions:
            print('session already exists')
            exit()
        else:
            self.sessions.update({mac: None})  # Instead of multithreading
            print('session ID: ', mac)
            self.sessions[mac] = Portal((self.session_exit, mac))

    def session_exit(self, mac):
        if mac in self.sessions:
            self.sessions.pop(mac)
            print('exited session: ', mac)
            exit()
        exit('exited code, no mac in session')


if __name__ == "__main__":
    session = Session()
    session.New_Session()
