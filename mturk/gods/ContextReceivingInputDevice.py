import Queue
import uuid

from system import system_channels

from devices import InputDevice
from MturkData import MturkData


class ContextReceivingInputDevice(InputDevice.AbstractInputDevice):
    """
    """
    def __init__(self, timeout_seconds = 0.5):
        super(ContextReceivingInputDevice, self).__init__()
        self.timeout_seconds = timeout_seconds
        self.received_inputs = Queue.Queue()

    def accept_context(self, conversation_id, new_context):
        """
            Accept a new input and add to the dispatched queue.
        """
        new_id = uuid.uuid4().hex
        new_input = MturkData(conversation_id, new_id, new_context)

        self.received_inputs.put(new_input)
        return new_id

    def accept_score(self, conversation_id, new_id, score):
        self.publish(MturkData(conversation_id, new_id, score), channel = system_channels.SCORING)

    def take_input(self):
        """
            Get inputs from the dispatched queue.
        """
        try:
            return [self.received_inputs.get(True, timeout = self.timeout_seconds)]
        except Queue.Empty:
            return None