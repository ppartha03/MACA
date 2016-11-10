import abc
from utils.abstract_designs import PubSub

class AbstractConversationListener(PubSub.Subscriber):
    """
        AbstractConversationListener: represent an abstract conversation listener that will listen to both the input and output of the system.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(AbstractConversationListener, self).__init__()
