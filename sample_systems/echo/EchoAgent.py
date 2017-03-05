from agents.AbstractAgent import AbstractAgent
from system import system_channels
from system import system_modes

import logging
logger = logging.getLogger(__name__)

class EchoAgent(AbstractAgent):
    """
        Simply echo the input to the output.
    """
    def __init__(self, domain_knowledge = None, mode = system_modes.EXECUTION):
        super(EchoAgent, self).__init__(domain_knowledge, mode)

    def process_inputs(self, inputs):
    	"""
    		Expecting a list of inputs. Each input is a list of preprocessed data.
    		This agent picks the first preprocessed data in the input.
    	"""
        if self.mode == system_modes.TRAINING:
            logger.info("Echo agent received inputs {} in training mode.".format(inputs))
            return [None]
        else:
            return [data[0] for data in inputs]


    def model_postprocess(self, outputs):
        for data in outputs:
            self.queue_output(data)

    def process_notification(self, content, channel):
        if channel == system_channels.TRAINING:
            logger.info("Training termination signal received.")
        else:
            logger.info("Agent received notification {0} on channel {1}.".format(content, channel))