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
        return [data[0] for data in inputs]


    def model_postprocess(self, outputs):
        for data in outputs:
            self.queue_output(data)

    def process_notification(self, content, channel):
        logger.info("Agent received notification {0} on channel {1}.".format(content, channel))