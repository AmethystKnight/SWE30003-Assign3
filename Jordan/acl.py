from constants import TKeys
from user_token import User_Token
from portal_interfaces import ITokenGuide


class ACL(ITokenGuide):
    def __init__(self):
        self._privileges = {'admin': 1, 'foh': 0, 'boh': 0}
        self._portals = None
        self._token = None

    def posses_token(self, user: User_Token):
        from portal import BusinessPortal, FOHPortal, BOHPortal

        self._portals = {'admin': BusinessPortal, 'foh': FOHPortal, 'boh': BOHPortal}

        if self._token is not None:
            print("ACL queue")
        self._token = user
        if TKeys.PortalKey not in user.data or TKeys.Privilege not in user.data:
            print("adding data via acl")
            user_name = self._token.data[TKeys.Username]
            self._token.data.update({TKeys.Privilege: self._privileges[user_name]})
            self._token.data.update({TKeys.PortalKey: self._portals[user_name]})
            print(self._token.data)

    def guide_token(self, next_guide: ITokenGuide) -> bool:
        privilege = self._token.data.get(TKeys.Privilege, -1)
        if privilege < next_guide.access_level():
            # print('current data', self._token.data)
            # print(privilege)
            # print(next_guide.access_level())
            print("You do not have access")
            return False
        else:
            next_guide.posses_token(self._token)
            return True

    def access_level(self) -> int:
        return 0
