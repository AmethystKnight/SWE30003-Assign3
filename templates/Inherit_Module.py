import queue
from abc import ABC
from abc import abstractmethod
from threading import Lock, Thread
# from Login import User_Token
from collections import deque
from enum import Enum

"""For mediator classes or junctions"""


class ITokenGuide(ABC):

    @abstractmethod
    def PossesToken(self, token: 'User_Token'):
        """Opportunity to alter the token by adding more data.
        You can do any non-trivial functional operations here."""
        pass

    @abstractmethod
    def GuideToken(self, next_guide: 'ITokenGuide'):
        """Pass on to next guide with their posses' method,
        gives a chance to clean up, _token = None"""
        pass

    @abstractmethod
    def AccessLevel(self) -> int:
        """The acl will need this to know if it's appropriate
        to pass the token to the next guide"""
        pass


"""
# I couldn't get it working with __call__
# reference: https://refactoring.guru/design-patterns/singleton/python/example
# configure thread safety after logic
"""


class Singleton:
    _instance = None
    _lock: Lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                # passing python type with singleton
                cls._instance = super().__new__(cls)
        # instead of returning a default py obj we return the instance
        return cls._instance


class Mediator(Singleton, ABC):
    """single mediator per operation; mediators jobs is to control the
     flow of msg data and is also responsible for sending that data to the
     correct recipients, each mediator should be responsible for one
     microservice or module(cluster of loosely coupled classes.)
     This is a virtual class, to be inherited by all mediators"""

    def __init__(self):
        super(Mediator, self).__init__()
        self._msg = None
        # thread safe collection
        self._queue = deque()  # FIFO
        self._lock = Lock()

    # make sure you only process one token at a time
    def Next_In_Thread_Queue(self):
        # convention for safe lock release
        with self._lock:
            if len(self._queue) > 0:
                self._msg = self._queue.pop()

    @abstractmethod
    def _Process_Logic(self, *args):
        """Mediators have the ability to pass signal to multiple recipients.
        NOTE: You ust use Next_In_Thread_Queue():, this will push the queue forward
        NOTE: this is a private class, use Send_Data() to push msg """

    # Append left for FIFO
    def Receive_Msg(self, msg):
        # convention for safe lock acquisition
        with self._lock:
            self._queue.appendleft(msg)

    def Send_Msg(self, *args):
        recipients = args
        self.Next_In_Thread_Queue()
        self._Process_Logic(recipients)


#   def print_msg(self):
#     print(self.msg)

# Test the singleton
# mediator1 = Mediator()
# mediator2 = Mediator()
# mediator1.msg = 'Hi'
# mediator2.msg = 'Its good'
# mediator1.print_msg()  # Output: Its good
# mediator2.print_msg()  # Output: Its good

import time

# from Login import LoginPortal, User_Token, TKeys
from threading import Event


class TKeys(Enum):
    Username = 0
    Password = 1
    Privilege = 2
    PortalKey = 3


from functools import partial


class Portal(ITokenGuide):
    """Main Portal, _portal is the current context"""

    def __init__(self, exit_func):

        self._exit = partial(exit_func[0], exit_func[1])  # sessions exit function
        self._token = None
        self._portal = None

        self.portal_commands = {'help': self._print_help, 'login': self.Login, 'exit': self._exit}

        self.Login()
        while True:
            user_in = input("type help for commands")

            if user_in in self.portal_commands:
                self.portal_commands.get(user_in)()
            else:
                print('invalid input')

    def _print_help(self):
        for key in self.portal_commands.keys():
            print(key)

    def PossesToken(self, user: 'User_Token'):
        self._token = user

    def GuideToken(self, next_guide: ITokenGuide):
        next_guide.GuideToken(self._token)

    def AccessLevel(self) -> int:
        return 0

    def Login(self):
        from Login import LoginPortal, User_Token, TKeys
        """Logs in user and instantiates portal once it is finished processing
               via ACL inside Login"""
        print('logging in..')
        self._portal = LoginPortal(self)
        if self._portal.Login():
            # thread safety
            # while self._token is None:
            #     time.sleep(0.1)
            self._token: User_Token
            # instantiates main Portal context
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
