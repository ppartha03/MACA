import abc
import datetime

class AbstractOutputDevice(object):
    """
        Abstract class for output devices
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(AbstractOutputDevice, self).__init__()

    @abc.abstractmethod
    def write_output(self, output):
        """
            Output a string
        """
        pass

class VoidOutputDevice(AbstractOutputDevice):
    """
        Does nothing to output.
    """

    def __init__(self):
        super(VoidOutputDevice, self).__init__()

    def write_output(self, output):
        pass

class StdoutOutputDevice(AbstractOutputDevice):
    """
        An output device that outputs to the stdout stream.
    """
    def __init__(self):
        super(StdoutOutputDevice, self).__init__()

    def write_output(self, output):
        print 'AI: {0}'.format(output.data if output else output)

class FileOutputDevice(AbstractOutputDevice):
    """
        An output device that outputs to a file.
    """
    def __init__(self, file_name, write_mode = 'a'):
        super(FileOutputDevice, self).__init__()
        self.file_object = open(file_name, write_mode)

    def write_output(self, output):
        prefix = datetime.datetime.now().strftime('[%d/%m/%Y][%H:%M:%S]')
        self.file_object.write('{0} - AI: {1}'.format(prefix, output.data if output else output))
        self.file_object.flush()