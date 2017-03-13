import sys

import cPickle
import traceback
import itertools
import logging
import time
from collections import namedtuple

import collections
import string
import os
import numpy
import codecs

import nltk
from random import randint

import theano

from system import system_modes

from sample_systems.hred import train

from sample_systems.hred import search
from sample_systems.hred.dialog_encdec import DialogEncoderDecoder
from sample_systems.hred.numpy_compat import argpartition
from sample_systems.hred.state import prototype_ubuntu_HRED #prototype_state

from sample_systems.hred import chat

from agents.AbstractAgent import AbstractAgent
from TextData import TextData

logger = logging.getLogger(__name__)

class HREDAgent(AbstractAgent):

    ### Additional measures can be set here
    measures = ["train_cost", "train_misclass", "train_kl_divergence_cost", "train_posterior_mean_variance", "valid_cost", "valid_misclass", \
                "valid_posterior_mean_variance", "valid_kl_divergence_cost", "valid_emi"]

    DEFAULT_TRAINING_CONFIG = {
        'resume' : '',
        'force_train_all_wordemb' : False,
        'save_every_valid_iteration' : False,
        'auto_restart' : False,
        'prototype' : 'prototype_ubuntu_HRED',
        'reinitialize_latent_variable_parameters' : False,
        'reinitialize_decoder_parameters' : False,
    }

    """
        Agent using HRED.
        Need to enable certain Theano flags when using.
        THEANO_FLAGS=mode=FAST_RUN,device=gpu,floatX=float32
    """
    def __init__(self, train_args = {},
                    ignore_unknown_words = True,
                    normalize = False,
                    dictionary_path = '/home/ml/rlowe1/UbuntuData/Dataset.dict.pkl',
                    model_prefix = '/home/2016/pparth2/Desktop/gods/Goal-Oriented_Dialogue_Systems/Pre-Trained_HRED_Model/drive-download-20161021T162213Z/1453999317.44_UbuntuModel_HRED/1453999317.44_UbuntuModel_HRED',
                    mode = system_modes.EXECUTION, domain_knowledge = None):
        super(HREDAgent, self).__init__(domain_knowledge, mode)

        if mode == system_modes.EXECUTION:
            state = prototype_ubuntu_HRED() #prototype_state()

            state_path = model_prefix + "_state.pkl"
            model_path = model_prefix + "_model.npz"

            with open(state_path) as src:
                state.update(cPickle.load(src))
            state['dictionary'] = dictionary_path

            self.ignore_unknown_words = ignore_unknown_words
            self.normalize = normalize

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
        elif mode == system_modes.TRAINING:
            configs = self.DEFAULT_TRAINING_CONFIG.copy()
            configs.update(train_args)
            Args = namedtuple('Args', configs.keys())

            self.args = Args(**configs)

    def model_preprocess(self, inputs):
        if self.mode == system_modes.EXECUTION:
            return [[ self.model.end_sym_utterance ] + ['<first_speaker>'] + data[0].data + [ self.model.end_sym_utterance ] for data in inputs]
        else:
            return None

    def process_inputs(self, inputs):
        if self.mode == system_modes.EXECUTION:
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
                    seqs= [seqs], ignore_unk=self.ignore_unknown_words, \
                    sampler=self.sampler, n_samples=1)

                if len(sentences) == 0:
                    raise ValueError("Generation error, no sentences were produced!")

                self.utterances.append(sentences[0][0].split())

                reply = sentences[0][0].encode('utf-8')
                outputs.append(reply)

            return outputs
        elif self.mode == system_modes.TRAINING:
            print "Here too"
            train.main(self.args)

    def model_postprocess(self, outputs):
        if self.mode == system_modes.EXECUTION:
            for output in outputs:
                self.queue_output(TextData(chat.remove_speaker_tokens(output)))
