from agents.AbstractAgent import AbstractAgent
from system import system_channels
from MturkData import MturkData

import logging
logger = logging.getLogger(__name__)

class MturkCollectionAgent(AbstractAgent):
    """
    """

    def __init__(self, domain_knowledge = None):
        super(MturkCollectionAgent, self).__init__(domain_knowledge)

    def process_inputs(self, inputs):
        """
            Does nothing. The response to the inputs will be provided by the front end client, which then invokes accept_response method to enqueue it.
        """
        return []

    def model_postprocess(self, outputs):
        """
            Nothing to post process.
        """
        pass

    def accept_response(self, conversation_id, response_id, response_data):
        """
            Accept a response from front end client. Immediately enqueue this response at the output queue.
        """

        self.queue_output(MturkData(conversation_id, response_id, response_data))

    def process_notification(self, content, channel):
        logger.info("Agent received notification {0} on channel {1}.".format(content, channel))
