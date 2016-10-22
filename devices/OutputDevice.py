import abc


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
        self.file_object.write('AI: {0}\n'.format(output.data if output else output))
        self.file_object.flush()