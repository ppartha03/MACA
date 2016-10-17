import time
import signal
import threading

import InputDevice
import OutputDevice
from EchoAgent import EchoAgent
from FlightBookingAgent import FlightBookingAgent

class MainObject(object):
    """
        Main object holding the InputTexts.
    """
    def __init__(self, input_device, output_device, agent):
        super(MainObject, self).__init__()
        self.terminate = False

        self.input_device = input_device
        self.output_device = output_device
        self.agent = agent

def input_loop(main_object):
    while not main_object.terminate:
        next_inputs = main_object.input_device.take_input()
        main_object.agent.process_inputs(next_inputs)

def output_loop(main_object):
    while not main_object.terminate:
        next_output = main_object.agent.next_output(timeout = None)
        main_object.output_device.write_output(next_output)


if __name__ == "__main__":
    agent = FlightBookingAgent()
    main_object = MainObject(InputDevice.StdinInputDevice(), OutputDevice.StdoutOutputDevice(), agent)

    inputs = threading.Thread(target = input_loop, args = (main_object, ))
    outputs = threading.Thread(target = output_loop, args = (main_object, ))

    def terminate():
        main_object.terminate = True

        inputs.join()
        outputs.join()

    signal.signal(signal.SIGTERM, terminate)

    inputs.start()
    outputs.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print "Terminating gods..."
        terminate()