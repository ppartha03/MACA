from preprocessing.AbstractPreprocessor import AbstractPreprocessor
from TextData import TextData

class HredPreprocessor(AbstractPreprocessor):
    """
        Simply split the input into tokens
    """
    def __init__(self):
        super(HredPreprocessor, self).__init__()

    def preprocess(self, data):
    	sentence = data.data

        return TextData(sentence.split())