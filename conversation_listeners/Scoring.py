import abc
from AbstractConversationListener import AbstractConversationListener

from system import system_channels
import logging
logger = logging.getLogger(__name__)

class Scoring(AbstractConversationListener):

    __metaclass__ = abc.ABCMeta

    """
        The scoring unit requires a scoring publisher, which will ensure the scoring reaches its subscribers.
    """

    def __init__(self):
        super(Scoring, self).__init__()
        self.scoring_publisher = None

    def _provide_feedback(self, scoring):
        assert self.scoring_publisher is not None
        self.scoring_publisher.publish(scoring, channel = 'scoring')

    @abc.abstractmethod
    def process_notification(self, content, channel):
        """
            Provide scoring using the private method denoted below.
        """
        pass


class SampleScoring(Scoring):

    def __init__(self):
        super(SampleScoring, self).__init__()

    def process_notification(self, content, channel):
        logger.info("Scoring module received {0} on channel {1}".format(content, channel))
        self._provide_feedback("Sample scoring provided for {0}".format(content))