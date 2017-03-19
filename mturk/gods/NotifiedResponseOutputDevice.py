from devices import OutputDevice

from TextData import TextData


class NotifiedResponseOutputDevice(OutputDevice.FileOutputDevice):
    """
        An output device that supports mturk receive server. Extension of FileOutputDevice.
    """
    def __init__(self, file_name):
        super(NotifiedResponseOutputDevice, self).__init__(file_name)
        self.events = {}
        self.responses = {}

    def register_response_event(self, new_id, event):
        self.events[new_id] = event

    def get_response(self, new_id):
        if new_id in self.responses:
            response = self.responses.pop(new_id)
            return response
        else:
            return None

    def write_output(self, output):
        """
            We expect an object of type MturkData here.
        """
        conversation_id = output.conversation_id
        response_id = output.context_id
        response_content = output.data

        if response_id in self.events:
            self.responses[response_id] = response_content

            event = self.events.pop(response_id)
            event.set()

        super(NotifiedResponseOutputDevice, self).write_output(TextData(response_content))