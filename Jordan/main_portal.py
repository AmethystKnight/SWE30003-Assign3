from portal_interfaces import ITokenGuide, Portal
from login_portal import LoginPortal
from constants import TKeys
from user_token import User_Token
from functools import partial

class MainPortal(ITokenGuide, Portal):
    """Main Portal, _portal is the current context"""

    def __init__(self, exit_func):
        self._exit = partial(exit_func[0], exit_func[1])
        self._token = None
        self._portal = None
        self._ui = None  # UI will be set later by the controller
        self.login()
        self._run()

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

    def _run(self):
        while True:
            user_in = self._ui.user_in()
            if user_in in self.portal_commands:
                self.portal_commands[user_in]()
            else:
                print('invalid input')


