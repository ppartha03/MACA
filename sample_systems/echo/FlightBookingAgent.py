from agents.AbstractAgent import AbstractAgent
from InformationState import AbstractInformationState
from TextData import TextData


class GreetingsState(AbstractInformationState):
    """docstring for GreetingsState"""
    def __init__(self, agent):
        super(GreetingsState, self).__init__()

    def extract_information(self, data):
        # Nothing to do here
        pass

class DateTimeState(AbstractInformationState):
    """
        At this state, we try to get date and time of the flight.
    """
    def __init__(self):
        super(DateTimeState, self).__init__()

    def extract_information(self, data):
        return TextData("This is a test. The input is {0}".format(data.data))

class FinishedState(AbstractInformationState):
    """
        At this state, we are done with the booking.
    """
    def __init__(self):
        super(FinishedState, self).__init__()

    def extract_information(self, data):
        return TextData('Flight booking confirmed.')

class FlightBookingAgent(AbstractAgent):
    """
        Simply echo the input to the output.
    """
    def __init__(self):
        super(FlightBookingAgent, self).__init__()
        self.current_state = GreetingsState(self)
        self.queue_output(TextData('Hi!'))

    def process_inputs(self, inputs):
        if type(self.current_state) is GreetingsState:
            self.current_state = DateTimeState()
            self.process_inputs(inputs)
        elif type(self.current_state) is DateTimeState:
            for data in inputs:
                response = self.current_state.extract_information(data)
                if response:
                    self.queue_output(response)
                    self.current_state = FinishedState()
        else:
            for data in inputs:
                self.queue_output(self.current_state.extract_information(data))

