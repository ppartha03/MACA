import logging
from AbstractConversationListener import AbstractConversationListener

logger = logging.getLogger(__name__)

class LoggingListener(AbstractConversationListener):
    """
        A listener that logs what it listens.
    """
    def __init__(self):
        super(LoggingListener, self).__init__()

    def process_notification(self, content, tag):
        logger.info("Content listened [{0}]: {1}".format(tag, content))
