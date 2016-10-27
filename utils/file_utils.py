import os
import imp

def load_module(file_name):
    """
        Load a python file as a module. Throw exception if file does not exist.

        file_name: path to the file to load.
    """
    assert os.path.isfile(file_name)

    parent_dir = os.path.dirname(file_name)
    raw_file_name = os.path.basename(file_name)
    raw_file_name = os.path.splitext(raw_file_name)[0] #Remove file extension

    return imp.load_source(raw_file_name, file_name)