import queue
from abc import ABC
from abc import abstractmethod
from threading import Lock, Thread
from Login import User_Token
from collections import deque

"""For mediator classes or junctions"""


class ITokenGuide(ABC):

    @abstractmethod
    def PossesToken(self, token: User_Token):
        """Opportunity to alter the token by adding more data.
        You can do any non-trivial functional operations here."""
        pass

    @abstractmethod
    def GuideToken(self, next_guide: 'ITokenGuide'):
        """Pass on to next guide with their posses' method,
        gives a chance to clean up, _token = None"""
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
