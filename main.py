import logging
import time
import signal
import threading

import Queue

from system import system
from utils import file_utils

from config import config

if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s][%(levelname)s][%(filename)s][%(lineno)d] - %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    filename='log.gods',
                    filemode='a',
                    level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    system_description = file_utils.load_module(config['system_description_file']).system_description
    system_object = system.System.construct_system(system_description)
    system_object.configure(config)

    inputs = threading.Thread(target = system_object.input_loop)
    outputs = threading.Thread(target = system_object.output_loop)

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