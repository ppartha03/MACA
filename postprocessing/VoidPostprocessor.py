from postprocessing.AbstractPostprocessor import AbstractPostprocessor

class VoidPostprocessor(AbstractPostprocessor):
    """
        Does nothing to the input.
    """
    def __init__(self):
        super(VoidPostprocessor, self).__init__()

    def postprocess(self, data):
        return data