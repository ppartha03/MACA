import nltk

import AbstractPreprocessor

class TokenizerPreprocessor(AbstractPreprocessor.AbstractPreprocessor):
    """
        A preprocessor that tokenizes sentence into a list of words.
    """

    def __init__(self):
        super(TokenizerPreprocessor, self).__init__()

    def preprocess(self, data):
        return nltk.word_tokenize(data.data)