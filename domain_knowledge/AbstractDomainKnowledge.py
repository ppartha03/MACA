import abc


class AbstractDomainKnowledge(object):
    """
        Abstract class for domain knowledge
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(AbstractDomainKnowledge, self).__init__()

        self.data = None # Data used to train/validate/test the model. See class AbstractDataSet below


class AbstractDataSet(object):
    """
        Abstract class for a data set. This class should be able to offer various operations for a data set so that we can easily
        train/validate/test a model.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(AbstractDataSet, self).__init__()

    @abc.abstractmethod
    def load_data(self):
        pass

    @abc.abstractmethod
    def get_training_data(self):
        pass

    @abc.abstractmethod
    def get_validation_data(self):
        pass

    @abc.abstractmethod
    def get_testing_data(self):
        pass