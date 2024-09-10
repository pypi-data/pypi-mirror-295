from multiprocessing import Pipe
from threading import Thread
import typing


class PoolThread:
    """A Class that starts a thread, to which one can add functions to
    be run in that thread. with the ``Thread`` class of the ``threading`` module,
    it is only possible to run a single target function in a thread, but instantiating
    a thread takes time, which can distort the functionality of the ``DetectorPool`` class"""

    def __init__(self):
        # self._thread = Thread(target=self.__worker, args=())
        self._thread: typing.Optional[Thread] = None

        c1, c2 = Pipe()
        self._c1 = c1
        self._c2 = c2

    def start(self) -> None:
        self._thread = Thread(target=self.__worker, args=())
        self._thread.start()

    def join(self):
        """Just like ``Thread.join()``."""
        # self.pass_function(None)
        self._c2.send((None, []))
        self._thread.join()
        self._thread = None

    def __worker(self):
        while True:
            function, args = self._c1.recv()
            if function is not None:
                function(*args)
            else:
                break

    def pass_function(self, function: typing.Callable, *args: typing.Any):
        if self._thread is None:
            self.start()
        """Pass a function to the thread."""
        self._c2.send((function, args))
