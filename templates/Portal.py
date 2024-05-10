import time

from Inherit_Module import ITokenGuide
from Login import LoginPortal, User_Token, TKeys
from threading import Event


class Portal(ITokenGuide):
    """Main Portal, _portal is the current context"""

    def __init__(self):
        self._token = None
        self._portal = None

    def PossesToken(self, user: User_Token):
        self._token = user

    def GuideToken(self, next_guide: ITokenGuide):
        next_guide.GuideToken(self._token)

    def Login(self):
        """Logs in user and instantiates portal once it is finished processing
               via ACL inside Login"""
        self._portal = LoginPortal(self)
        if self._portal.Login():
            # thread safety
            while self._token is None:
                time.sleep(0.1)
            self._token: User_Token
            # instantiates main Portal context
            self._portal = self._token.data[TKeys.PortalKey]()


class FOHPortal:
    pass


class BOHPortal:
    pass


class BusinessPortal:
    pass
