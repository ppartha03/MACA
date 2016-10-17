import abc


class AbstractOutputDevice(object):
    """docstring for AbstractOutputDevice"""

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(AbstractOutputDevice, self).__init__()

    @abc.abstractmethod
    def write_output(self, output):
        """
            Output a string
        """
        pass

class StdoutOutputDevice(AbstractOutputDevice):
    """docstring for StdoutOutputDevice"""
    def __init__(self):
        super(StdoutOutputDevice, self).__init__()

    def write_output(self, output):
        print 'Response: {0}'.format(output.data if output else output)