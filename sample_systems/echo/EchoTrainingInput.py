from system import system_channels

from devices import InputDevice
from TextData import TextData

class EchoTrainingInput(InputDevice.AbstractInputDevice):
    """
        Provide a sample list of inputs stored in memory.
    """
    def __init__(self, max_epochs = 1000):
        super(EchoTrainingInput, self).__init__()
        self.data = [
            'Hello',
            'How are you?',
            'What is the fastest animal?'
        ]
        self.index = 0
        self.epoch = 0
        self.max_epochs = max_epochs

    def take_input(self):
        output = [TextData(self.data[self.index])]
        self.index = (self.index + 1) % len(self.data)

        if self.index == 0:
            self.epoch += 1

        if self.epoch == self.max_epochs:
            self.publish('Terminate', system_channels.TRAINING)

            raise Exception("Training finished. Terminating input thread.")

        return output
