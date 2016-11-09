import logging
import time
import signal
import threading
import traceback

import Queue

import system
from utils import file_utils

from config import config

def input_loop(system_object):
    while not system_object.terminate:
        raw_inputs = system_object.input_device.take_input()
        system_object.listeners.listen_to_inputs(raw_inputs)

        processed_inputs = [system_object.preprocessing.preprocess(data) for data in raw_inputs]
        system_object.agent.process_inputs(processed_inputs)

def output_loop(system_object):
    while not system_object.terminate:
        try:
            next_output = system_object.agent.next_output(timeout = config['io_timeout'])
            if next_output:
                processed_outputs = system_object.postprocessing.postprocess(next_output)
                system_object.listeners.listen_to_output(processed_outputs)

                to_write = system_object.postprocessing.get_output(processed_outputs)

                system_object.output_device.write_output(to_write)
        except: # Notify exception
            traceback.print_exc()


if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s][%(levelname)s][%(filename)s][%(lineno)d] - %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filename='log.gods',
                    filemode='a',
                    level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    system_description = file_utils.load_module(config['system_description_file']).system_description
    system_object = system.System.construct_system(system_description)

    inputs = threading.Thread(target = input_loop, args = (system_object, ))
    outputs = threading.Thread(target = output_loop, args = (system_object, ))

    def terminate():
        system_object.terminate = True

        inputs.join()
        print("Terminated input loop...")
        outputs.join()
        print("Terminated output loop...")

    signal.signal(signal.SIGTERM, terminate)

    inputs.start()
    outputs.start()

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Terminating gods...")
        terminate()
        print("Terminating main thread...")