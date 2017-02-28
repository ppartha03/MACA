import cPickle

from preprocessing import AbstractPreprocessor

from sample_systems.retrieval_model.BPE import apply_bpe

class RetrievalModelPreprocessor(AbstractPreprocessor.AbstractPreprocessor):
    """
        Apply BPE processing to the sentence.
        bpe_file: path to file containing bpe codes. E.g. Twitter_Codes_5000.txt
    """
    def __init__(self, bpe_file):
        super(RetrievalModelPreprocessor, self).__init__()
        self.bpe = apply_bpe.BPE(open(bpe_file, 'r').readlines())


    def preprocess(self, data):
        """
            Parameters
            ----------
            data : a pair of (context, response).

            Returns
            -------
            Same pair but after being processed by BPE module.
        """
        sentence_pair = data.data
        raw_context = sentence_pair[0]
        raw_response = sentence_pair[1]

        bpe_segments = self.bpe.segment(raw_context), self.bpe.segment(raw_response)
        return bpe_segments
