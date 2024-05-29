from abc import ABC, abstractmethod


class ITokenGuide(ABC):
    @abstractmethod
    def posses_token(self, token: 'User_Token'):
        """Opportunity to alter the token by adding more data.
        You can do any non-trivial functional operations here."""
        pass

    @abstractmethod
    def guide_token(self, next_guide: 'ITokenGuide'):
        """Pass on to next guide with their posses' method,
        gives a chance to clean up, _token = None"""
        pass

    @abstractmethod
    def access_level(self) -> int:
        """The acl will need this to know if it's appropriate
        to pass the token to the next guide"""
        pass


class Portal(ABC):
    """Defines type Portal,
    Defined as: object that can return data for a parallel ui_container"""
    # TODO: Can possibly add ui field
    pass
