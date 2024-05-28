from abc import ABC, abstractmethod
from collections import deque
from threading import Lock

from singleton import Singleton


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
