from agents.AbstractAgent import AbstractAgent

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
