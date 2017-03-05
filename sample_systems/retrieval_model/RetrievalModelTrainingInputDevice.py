import cPickle

from system import system_channels

from devices.InputDevice import AbstractInputDevice
from TextData import TextData

class RetrievalModelTrainingInputDevice(AbstractInputDevice):
    """
        Input device used for training retrieval model.
    """
    def __init__(self, n_epochs = 1, shuffle_batch = False):
        super(RetrievalModelTrainingInputDevice, self).__init__()
        self.n_epochs = n_epochs
        self.shuffle_batch = shuffle_batch
        self.epoch = 0

    def take_input(self):
        # return [TextData((next_line, another_line))]

        if self.epoch < self.n_epochs:
            self.epoch += 1

            return [{ 'shuffle_batch' : self.shuffle_batch, 'epoch' : self.epoch }]
        else:
            self.publish('save_model', system_channels.TRAINING)
            raise Exception("Training finished.")
