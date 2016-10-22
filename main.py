import logging
import time
import signal
import threading
import traceback

import Queue

from devices import InputDevice
from devices import OutputDevice
from agents.sample_agents.EchoAgent import EchoAgent
from agents.hred.gods_agent import hred_agent

from config import config

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
        try:
            next_output = main_object.agent.next_output(timeout = config['io_timeout'])
            if next_output:
                main_object.output_device.write_output(next_output)
        except: # Notify exception
            traceback.print_exc()


if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s][%(levelname)s][%(filename)s][%(lineno)d] - %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filename='log.gods',
                    filemode='a',
                    level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    input_device = InputDevice.StdinInputDevice()
    output_device = OutputDevice.FileOutputDevice('out.gods')
    agent = hred_agent.HREDAgent()

    main_object = MainObject(input_device, output_device, agent)

    inputs = threading.Thread(target = input_loop, args = (main_object, ))
    inputs.daemon = True
    outputs = threading.Thread(target = output_loop, args = (main_object, ))
    outputs.daemon = True

    def terminate():
        main_object.terminate = True

        inputs.join()
        print "Terminated input loop..."
        outputs.join()
        print "Terminated output loop..."

    signal.signal(signal.SIGTERM, terminate)

    inputs.start()
    outputs.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print "Terminating gods..."
        terminate()
        print "Terminating main thread..."