import abc
import sys
from select import select

from utils.abstract_designs import PubSub

from config import config
from TextData import TextData

class AbstractInputDevice(PubSub.Publisher):
    """
        AbstractInputDevice: represent an abstract natural language input source (e.g. voice, cmd line, ...)
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(AbstractInputDevice, self).__init__()

    @abc.abstractmethod
    def take_input(self):
        """
            Returns
            -------
            All user input from previous time input has been taken as a list of TextData.
        """
        pass

class StdinInputDevice(AbstractInputDevice):
    """docstring for StdinInputDevice"""
    def __init__(self):
        super(StdinInputDevice, self).__init__()

    def stdin_with_timeout(self, timeout):
        print "---> ",
        sys.stdout.flush()

        rlist, _, _ = select([sys.stdin], [], [], timeout)
        if rlist:
            data = sys.stdin.readline()
            return data
        else:
            print ""
            return None

    def take_input(self):
        data = self.stdin_with_timeout(config['io_timeout'])
        if data:
            return [TextData(data)]
        else:
            return []