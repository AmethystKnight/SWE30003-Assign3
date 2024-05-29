import uuid
from multiprocessing import Process
from singleton import Singleton
from acl import ACL
from portal import MainPortal

class Session(Singleton):
    from multiprocessing import Process
    """Session uses mac as an id, because it would be unique inside your network,
    this is not intended for a global program but one that is run locally and does not want to double up
    on logins on the same device"""
    def __init__(self):
        super(Session, self).__init__()
        self.sessions = {}
        self.acl = ACL()

    def new_session(self):
        """The idea is to hide the mac in the meta deta as much as possible"""
        mac = hex(uuid.getnode())
        if mac in self.sessions:
            print('session already exists')
            exit()
        else:
            self.sessions.update({mac: None})
            print('session ID: ', mac)
            self.sessions[mac] = MainPortal((self.session_exit, mac))

    def session_exit(self, mac):
        if mac in self.sessions:
            self.sessions.pop(mac)
            print('exited session: ', mac)
            exit()
        exit('exited code, no mac in session')
