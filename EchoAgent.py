from AbstractAgent import AbstractAgent

class EchoAgent(AbstractAgent):
    """
        Simply echo the input to the output.
    """
    def __init__(self):
        super(EchoAgent, self).__init__()

    def process_inputs(self, inputs):
        for data in inputs:
            self.queue_output(data)
