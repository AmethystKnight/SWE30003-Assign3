from abc import ABC, abstractmethod

class ITokenGuide(ABC):
    @abstractmethod
    def posses_token(self, token: 'User_Token'):
        pass

    @abstractmethod
    def guide_token(self, next_guide: 'ITokenGuide'):
        pass

    @abstractmethod
    def access_level(self) -> int:
        pass
