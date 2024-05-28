import uuid
from multiprocessing import Process
from singleton import Singleton
from acl import ACL
from portal import Portal

class Session(Singleton):
    def __init__(self):
        super(Session, self).__init__()
        self.sessions = {}
        self.acl = ACL()

    def new_session(self):
        mac = hex(uuid.getnode())
        if mac in self.sessions:
            print('session already exists')
            exit()
        else:
            self.sessions.update({mac: None})
            print('session ID: ', mac)
            self.sessions[mac] = Portal((self.session_exit, mac))

    def session_exit(self, mac):
        if mac in self.sessions:
            self.sessions.pop(mac)
            print('exited session: ', mac)
            exit()
        exit('exited code, no mac in session')
