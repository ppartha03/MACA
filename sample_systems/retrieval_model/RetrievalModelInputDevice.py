from devices.InputDevice import AbstractInputDevice
from TextData import TextData

class RetrievalModelInputDevice(AbstractInputDevice):
    """
        Input device that reads from file two lines at a time.
    """
    def __init__(self, file_name, read_mode = 'r'):
        super(RetrievalModelInputDevice, self).__init__()

        self.reader = open(file_name, read_mode)

    def take_input(self):
        try:
            next_line = next(self.reader)
            another_line = next(self.reader)
            return [TextData((next_line, another_line))]
        except StopIteration: # End of file
            self.reader.close()
            raise Exception("End of input stream.")