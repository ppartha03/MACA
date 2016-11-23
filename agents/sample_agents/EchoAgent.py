from agents.AbstractAgent import AbstractAgent

import logging
logger = logging.getLogger(__name__)

class EchoAgent(AbstractAgent):
    """
        Simply echo the input to the output.
    """
    def __init__(self):
        super(EchoAgent, self).__init__()

    def process_inputs(self, inputs):
    	"""
    		Expecting a list of inputs. Each input is a list of preprocessed data.
    		This agent picks the first preprocessed data in the input.
    	"""

        for data in inputs:
            self.queue_output(data[0])

    def process_notification(self, content, channel):
        logger.info("Agent received notification {0} on channel {1}.".format(content, channel))