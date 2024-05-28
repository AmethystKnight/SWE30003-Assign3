from functools import partial
from portal_interfaces import ITokenGuide
from login_portal import LoginPortal
from constants import TKeys
from user_token import User_Token

class Portal(ITokenGuide):
    """Main Portal, _portal is the current context"""
    def __init__(self, exit_func):
        self._exit = partial(exit_func[0], exit_func[1])
        self._token = None
        self._portal = None

        self.portal_commands = {'help': self._print_help, 'login': self.login, 'exit': self._exit}

        self.login()
        while True:
            user_in = input("type help for commands")
            if user_in in self.portal_commands:
                self.portal_commands.get(user_in)()
            else:
                print('invalid input')

    def _print_help(self):
        for key in self.portal_commands.keys():
            print(key)

    def posses_token(self, user: 'User_Token'):
        self._token = user

    def guide_token(self, next_guide: ITokenGuide):
        next_guide.guide_token(self._token)

    def access_level(self) -> int:
        return 0

    def login(self):
        print('logging in..')
        self._portal = LoginPortal(self)
        if self._portal.login():
            self._token: User_Token
            self._portal = self._token.data[TKeys.PortalKey]()
            print("Login Successful")

class FOHPortal:
    def __init__(self):
        print("Front of House Portal Access")

class BOHPortal:
    def __init__(self):
        print("Back of House Portal Access")

class BusinessPortal:
    def __init__(self):
        print("Business Portal Access")
