import abc

class AbstractConversationListener(object):
    """
        AbstractConversationListener: represent an abstract conversation listener that will listen to both the input and output of the system.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(AbstractConversationListener, self).__init__()

    @abc.abstractmethod
    def listen_to_input(self, input):
        """
            Raw input.
        """
        pass

    @abc.abstractmethod
    def listen_to_output(self, output):
        """
            Postprocessed output channels.
        """
        pass