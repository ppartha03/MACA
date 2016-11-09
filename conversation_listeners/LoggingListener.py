import logging
from AbstractConversationListener import AbstractConversationListener

logger = logging.getLogger(__name__)

class LoggingListener(AbstractConversationListener):
    """
        A listener that logs what it listens.
    """
    def __init__(self):
        super(LoggingListener, self).__init__()

    def listen_to_input(self, inputs):
        """
            Preprocessed input channels.
        """
        logger.info("Input listened: {0}".format(inputs))

    def listen_to_output(self, outputs):
        """
            Postprocessed output channels.
        """
        logger.info("Output listened: {0}".format(outputs))