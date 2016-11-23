import abc
from AbstractConversationListener import AbstractConversationListener

from system import system_channels
import logging
logger = logging.getLogger(__name__)

class Feedback(AbstractConversationListener):

    __metaclass__ = abc.ABCMeta

    """
        The feedback unit requires a feedback publisher, which will ensure the feedback reaches its subscribers.
    """

    def __init__(self):
        super(Feedback, self).__init__()
        self.feedback_publisher = None

    def _provide_feedback(self, feedback):
        assert self.feedback_publisher is not None
        self.feedback_publisher.publish(feedback, channel = 'feedback')

    @abc.abstractmethod
    def process_notification(self, content, channel):
        """
            Provide feedback using the private method denoted below.
        """
        pass


class SampleFeedback(Feedback):

    def __init__(self):
        super(SampleFeedback, self).__init__()

    def process_notification(self, content, channel):
        logger.info("Feedback module received {0} on channel {1}".format(content, channel))
        self._provide_feedback("Sample feedback provided for {0}".format(content))