import abc
from TextData import TextData

class AbstractInputDevice(object):
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

    def take_input(self):
        data = raw_input('---> ')
        return [TextData(data)]