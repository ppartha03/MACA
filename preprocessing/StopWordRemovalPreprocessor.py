import nltk

import AbstractPreprocessor

class StopWordRemovalPreprocessor(AbstractPreprocessor.AbstractPreprocessor):
    """
        A preprocessor that removes stop words from the sentence.
        This returns the sentence as a string with stop words removed.
    """

    def __init__(self, language = 'english'):
        super(StopWordRemovalPreprocessor, self).__init__()
        self.language = language

    def preprocess(self, data):
    	split_data = [word for word in data.data.split(' ') if word not in nltk.corpus.stopwords(self.language)]
        return ' '.join(split_data)