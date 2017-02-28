import logging
import traceback
import argparse
import os
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

    parser = argparse.ArgumentParser(description = 'Track files and directories for changes')
    parser.add_argument('-f', '--config-file', dest='config_file', default=config['system_description_file'], help='Path to config file.', type = str)
    args = parser.parse_args()

    assert os.path.isfile(args.config_file)

    system_description = file_utils.load_module(args.config_file).system_description
    system_object = system.System.construct_system(system_description)
    system_object.configure(config)

    # inputs = threading.Thread(target = system_object.input_loop)
    # outputs = threading.Thread(target = system_object.output_loop)
    main_loop = threading.Thread(target = system_object.run)

    def terminate():
        system_object.terminate = True

        # inputs.join()
        # print("Terminated input loop...")
        # outputs.join()
        # print("Terminated output loop...")
        main_loop.join()
        print("Terminated main loop...")

    signal.signal(signal.SIGTERM, terminate)

    # inputs.start()
    # outputs.start()
    main_loop.start()

    try:
        # If use cusom main function, provide the system object.
        if 'main_function' in config:
            config['main_function'](system_object)
        else:
            while True:
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("Terminating gods...")
        terminate()
        print("Terminating main thread...")
    except:
        message = traceback.format_exc()
        logger.critical(message)
        print("Encountered exception when running main function.")
        terminate()
        print("Terminating main thread...")

    terminate() # Do it again in case the main function caught the interrupt signal
    print("System terminated!")
