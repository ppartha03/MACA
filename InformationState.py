import abc


class AbstractInformationState(object):
    """docstring for AbstractInformationState"""

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(AbstractInformationState, self).__init__()

    @abc.abstractmethod
    def extract_information(self, data):
        """
            Extract information from this input.
            This should involves extracting any content from the text input.

			Parameters
			----------
            data : a single TextData object

            Returns
            -------
            A TextData object representing the response, or None if there is no response.
        """
        pass

