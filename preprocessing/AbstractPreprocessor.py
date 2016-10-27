import abc

class AbstractPreprocessor(object):
    """
        AbstractPreprocessor: represent an abstract text data preprocessor.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(AbstractPreprocessor, self).__init__()

    @abc.abstractmethod
    def preprocess(self, data):
        """
			Input:
			A TextData object

            Returns
            -------
            The preprocessed data object.
        """
        pass