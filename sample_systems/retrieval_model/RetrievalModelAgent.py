import sys
import cPickle

from config import config
sys.path.insert(0, config['theano_path'])
import theano

from agents.AbstractAgent import AbstractAgent

import numpy as np
from sample_systems.retrieval_model import main
from TextData import TextData

import logging
logger = logging.getLogger(__name__)

class RetrievalModelAgent(AbstractAgent):
    """
        Implementation of retrieval model (dual encoder) agent.
        Adoption of implementation from https://github.com/NicolasAG/Discriminator

        Need to enable certain Theano flags when using.
        THEANO_FLAGS=mode=FAST_RUN,device=gpu,floatX=float32

        weight_path: path to file containing the preloaded weight and the dictionary from bpe words to index. E.g. W_twitter_bpe.pkl
    """

    DEFAULT_MODEL_CONFIGS = {
        'data' : None,
        'W' : None, # Has to be loaded at runtime
        'conv_attn' :  False,
        'encoder' : 'rnn',
        'hidden_size' : 200,
        'fine_tune_W' :  False,
        'fine_tune_M' :  False,
        'batch_size' : 256,
        'is_bidirectional' :  False,
        'lr_decay' : 0.95,
        'sqr_norm_lim' : 1,
        'lr' : 0.001,
        'optimizer' : 'adam',
        'forget_gate_bias' : 2.0,
        'max_seqlen' : 160,
        'corr_penalty' : 0.0,
        'xcov_penalty' : 0.0,
        'n_recurrent_layers' : 1,
        'penalize_emb_norm' :  False,
        'penalize_emb_drift' :  False,
        'penalize_activations' :  False,
        'emb_penalty' : 0.001,
        'act_penalty' : 500,
        'use_ntn' :  False,
        'k' : 4
    }

    def __init__(self, weight_path, model_params = {}, domain_knowledge = None):
        super(RetrievalModelAgent, self).__init__(domain_knowledge)
        W, self.index_dictionary = cPickle.load(open(weight_path, 'rb'))

        config = self.DEFAULT_MODEL_CONFIGS.copy()
        config['W'] = W.astype(theano.config.floatX)
        config.update(model_params)

        self.model = main.Model(**config)

    def process_inputs(self, inputs):
        """
            Feed input to internal model.

            Parameters
            ----------
            inputs : a list of pairs of (context, response).

            Returns
            -------
            A list of array, each array has size of batch size. Each entry of each array is the model prediction on whether the context fits with the given response.
            If there are more input rows than batch size, there will be multiple matrices at output.
        """
        data = {'c' : [row[0] for row in inputs], 'r' : [row[1] for row in inputs], 'y' : [1] * len(inputs)}

        loop_count = 1 + (len(inputs) // self.model.batch_size)

        results = []
        for i in xrange(loop_count):
            self.model.set_shared_variables(data, i)
            results.append(self.model.get_pred())

        return TextData(results)

    def model_preprocess(self, inputs):
        """
            For each pair of (context, response), lookup the appropriate index of the word in the dictionary.

            Parameters
            ----------
            inputs : a list of pairs of (context, response).

            Returns
            -------
            Same list of pairs but words are replaced by their respective indices in the dictionary.
        """
        inputs = inputs[0] # Only take the first preprocessed data
        return [[[self.index_dictionary.get(word, 0) for word in segment.split()] for segment in bpe_segments] for bpe_segments in inputs]

    def model_postprocess(self, outputs):
        if outputs is None:
            return

        self.queue_output(outputs)

    def process_notification(self, content, channel):
        logger.info("Agent received notification {0} on channel {1}.".format(content, channel))