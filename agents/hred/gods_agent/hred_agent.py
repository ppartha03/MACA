import sys
from config import config
sys.path.insert(0, config['theano_path'])


import cPickle
import traceback
import itertools
import logging
import time

import collections
import string
import os
import numpy
import codecs

import nltk
from random import randint

import theano

from agents.hred import search
from agents.hred.dialog_encdec import DialogEncoderDecoder
from agents.hred.numpy_compat import argpartition
from agents.hred.state import prototype_ubuntu_HRED #prototype_state

from agents.hred import chat

from agents.AbstractAgent import AbstractAgent
from TextData import TextData

logger = logging.getLogger(__name__)

class HREDAgent(AbstractAgent):
    """
        Agent using HRED.
        Need to enable certain Theano flags when using.
        THEANO_FLAGS=mode=FAST_RUN,device=gpu,floatX=float32
    """
    def __init__(self, domain_knowledge = None):
        super(HREDAgent, self).__init__(domain_knowledge)
        state = prototype_ubuntu_HRED() #prototype_state()

        state_path = config['model_prefix'] + "_state.pkl"
        model_path = config['model_prefix'] + "_model.npz"

        with open(state_path) as src:
            state.update(cPickle.load(src))
        state['dictionary'] = config['dictionary_path']

        # MODIFIED: Removed since configuring logging has to be before construction of any logging object
        # logging.basicConfig(level=getattr(logging, state['level']), format="%(asctime)s: %(name)s: %(levelname)s: %(message)s")

        self.model = DialogEncoderDecoder(state)
        if os.path.isfile(model_path):

            logger.debug("Loading previous model")
            self.model.load(model_path)
        else:
            raise Exception("Must specify a valid model path")

        logger.info("This model uses " + self.model.decoder_bias_type + " bias type")

        #self.sampler = search.RandomSampler(model)
        self.sampler = search.BeamSampler(self.model)

        # Start chat loop
        self.utterances = collections.deque()

    def model_preprocess(self, inputs):
        return [[ self.model.end_sym_utterance ] + ['<first_speaker>'] + data[0].data + [ self.model.end_sym_utterance ] for data in inputs]

    def process_inputs(self, inputs):
        outputs = []

        for current_utterance in inputs:
            # Increase number of utterances. We just set it to zero for simplicity so that model has no memory.
            # But it works fine if we increase this number
            while len(self.utterances) > 0:
                self.utterances.popleft()

            self.utterances.append(current_utterance)

            #TODO Sample a random reply. To spice it up, we could pick the longest reply or the reply with the fewest placeholders...
            seqs = list(itertools.chain(*self.utterances))

            #TODO Retrieve only replies which are generated for second speaker...
            sentences = chat.sample(self.model, \
                seqs= [seqs], ignore_unk=config['ignore_unknown_words'], \
                sampler=self.sampler, n_samples=1)

            if len(sentences) == 0:
                raise ValueError("Generation error, no sentences were produced!")

            self.utterances.append(sentences[0][0].split())

            reply = sentences[0][0].encode('utf-8')
            outputs.append(reply)

        return outputs

    def model_postprocess(self, outputs):
        for output in outputs:
            self.queue_output(TextData(chat.remove_speaker_tokens(output)))
