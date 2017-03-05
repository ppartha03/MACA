import Queue
import uuid

from system import system_channels

from devices import InputDevice
from TextData import TextData


class ContextReceivingInputDevice(InputDevice.AbstractInputDevice):
    """
    """
    def __init__(self, timeout_seconds = 0.5):
        super(ContextReceivingInputDevice, self).__init__()
        self.timeout_seconds = timeout_seconds
        self.received_inputs = Queue.Queue()

    def accept_context(self, new_context):
        """
            Accept a new input and add to the dispatched queue.
        """
        new_id = uuid.uuid4().hex
        self.received_inputs.put({
            'id' : new_id,
            'data' : new_context
            })
        return new_id

    def accept_score(self, new_id, score):
        print "here"
        self.publish({
                'id' : new_id,
                'score' : score
            }, channel = system_channels.INPUT)

    def take_input(self):
        """
            Get inputs from the dispatched queue.
        """
        try:
            return [self.received_inputs.get(True, timeout = self.timeout_seconds)]
        except Queue.Empty:
            return None