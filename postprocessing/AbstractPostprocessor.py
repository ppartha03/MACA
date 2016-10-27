import abc

class AbstractPostprocessor(object):
    """
        AbstractPostprocessor: represent an abstract data postprocessor (i.e. convert to text).
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(AbstractPostprocessor, self).__init__()

    @abc.abstractmethod
    def postprocess(self, data):
        """
			Input:
			A TextData object

            Returns
            -------
            The processed data object.
        """
        pass