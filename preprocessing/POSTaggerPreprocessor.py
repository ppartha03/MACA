import nltk

import AbstractPreprocessor

class POSTaggerPreprocessor(AbstractPreprocessor.AbstractPreprocessor):
    """
        A preprocessor that does part of speech (POS) tagging using nltk library without stop words removal.
        This returns the sentence split into tokens with POS tags.
    """

    def __init__(self):
        super(StopWordRemovalPreprocessor, self).__init__()

    def preprocess(self, data):
        sentence = data.data
        tokens = nltk.word_tokenize(sentence)
        return nltk.pos_tag(tokens)
