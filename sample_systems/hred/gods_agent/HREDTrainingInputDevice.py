from system import system_channels

from devices.InputDevice import AbstractInputDevice
from TextData import TextData

class HREDTrainingInputDevice(AbstractInputDevice):
    """
        Input device used for training hred model.
    """
    def __init__(self):
        super(HREDTrainingInputDevice, self).__init__()
        self.count = 0

    def take_input(self):
        # return [TextData((next_line, another_line))]

        if self.count == 1:
        	raise Exception("Training terminated")

        self.count += 1
        return [TextData("Start")]
