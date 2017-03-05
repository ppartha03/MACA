import sys
import time
import cPickle

from config import config
sys.path.insert(0, config['theano_path'])
import theano
import numpy as np
import lasagne

from system import system_modes
from system import system_channels
from agents.AbstractAgent import AbstractAgent
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

    def __init__(self, weight_path, model_params = {}, model_fname = 'model.pkl', mode = system_modes.EXECUTION, domain_knowledge = None):
        super(RetrievalModelAgent, self).__init__(domain_knowledge, mode)
        W, self.index_dictionary = cPickle.load(open(weight_path, 'rb'))

        config = self.DEFAULT_MODEL_CONFIGS.copy()
        config['W'] = W.astype(theano.config.floatX)
        config.update(model_params)

        self.model = main.Model(**config)

        if mode == system_modes.TRAINING:
            self.model_fname = model_fname
            self.best_val_perf = 0
            self.test_perf = 0
            self.test_probas = None

            # self.n_train_batches = len(self.train_data['y']) // self.batch_size
            # self.n_val_batches = len(self.validation_data['y']) // self.batch_size
            # self.n_test_batches = len(self.test_data['y']) // self.batch_size

            self.n_train_batches = 2 # min(2, n_train_batches)
            self.n_val_batches = 2 # min(2, n_val_batches)
            self.n_test_batches = 2 # min(2, n_test_batches)

            self.test_perf = 0
            self.test_probas = None

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

        if self.mode == system_modes.EXECUTION:
            data = {'c' : [row[0] for row in inputs], 'r' : [row[1] for row in inputs], 'y' : [1] * len(inputs)}

            loop_count = 1 + (len(inputs) // self.model.batch_size)

            results = []
            for i in xrange(loop_count):
                self.model.set_shared_variables(data, i)
                results.append(self.model.get_pred())

            return TextData(results)
        elif self.mode == system_modes.TRAINING:
            indices = range(self.n_train_batches)
            epoch = inputs['epoch']
            shuffle_batch = inputs['shuffle_batch']

            train_data = self.domain_knowledge.dataset.get_training_data()
            validation_data = self.domain_knowledge.dataset.get_training_data()
            test_data = self.domain_knowledge.dataset.get_testing_data()

            if shuffle_batch:
                indices = np.random.permutation(indices)

            total_cost = 0
            start_time = time.time()

            for minibatch_index in indices:
                self.model.set_shared_variables(train_data, minibatch_index)
                cost_epoch = self.model.train_model()
                # logger.info("cost epoch:", cost_epoch)
                total_cost += cost_epoch
                self.model.set_zero(self.model.zero_vec)

            end_time = time.time()
            logger.info("cost: {} took: {}(s)".format(total_cost / len(indices), end_time - start_time))

            # Compute TRAIN performance:
            train_losses = [self.model.compute_loss(train_data, i) for i in xrange(self.n_train_batches)]
            train_perf = 1 - np.sum(train_losses) / len(train_data['y'])
            logger.info("epoch %i, train perf %f" % (epoch, train_perf*100))
            # evaluation for each model id in train_data['id']
            # MODIFIED
            # self.model.compute_performace_models("train")

            # Compute VALIDATION performance:
            val_losses = [self.model.compute_loss(validation_data, i) for i in xrange(self.n_val_batches)]
            self.val_perf = 1 - np.sum(val_losses) / len(validation_data['y'])
            logger.info('epoch %i, val_perf %f' % (epoch, self.val_perf*100))
            # evaluation for each model id in validation_data['id']
            # MODIFIED
            # self.model.compute_performace_models("val")

            # If doing better on validation set:
            if self.val_perf > self.best_val_perf:
                logger.info("\nImproved validation score!")
                self.best_val_perf = self.val_perf
                # Compute TEST performance:
                test_losses = [self.model.compute_loss(test_data, i) for i in xrange(self.n_test_batches)]
                self.test_perf = 1 - np.sum(test_losses) / len(test_data['y'])
                logger.info('epoch %i, test_perf %f' % (epoch, self.test_perf*100))
                # evaluation for each model id in test_data['id']
                # MODIFIED
                # self.model.compute_performace_models("test")

                # Save current best model parameters.
                logger.info("\nSaving current model parameters...")
                with open('weights_%s_best.pkl' % self.model.encoder, 'wb') as handle:
                    params = [np.asarray(p.eval()) for p in lasagne.layers.get_all_params(self.model.l_out)]
                    cPickle.dump(params, handle)
                with open('embed_%s_best.pkl' % self.model.encoder, 'wb') as handle:
                    cPickle.dump(self.model.embeddings.eval(), handle)
                with open('M_%s_best.pkl' % self.model.encoder, 'wb') as handle:
                    cPickle.dump(self.model.M.eval(), handle)
                logger.info("Saved.\n")

            # return test_perf, test_probas
            return None # No output for training

    def model_preprocess(self, inputs):
        """
            For each pair of (context, response), lookup the appropriate index of the word in the dictionary.

            Parameters
            ----------
            inputs : a list of pairs of (context, response).

            Returns2
            -------
            Same list of pairs but words are replaced by their respective indices in the dictionary.
        """
        inputs = inputs[0] # Only take the first preprocessed data

        if self.mode == system_modes.EXECUTION:
            return [[[self.index_dictionary.get(word, 0) for word in segment.split()] for segment in bpe_segments] for bpe_segments in inputs]
        elif self.mode == system_modes.TRAINING:
            return inputs[0]

    def model_postprocess(self, outputs):
        if outputs is None:
            return

        self.queue_output(outputs)

    def process_notification(self, content, channel):
        # logger.info("Agent received notification {0} on channel {1}.".format(content, channel))
        if channel == system_channels.TRAINING:
            logger.info("Model trained...")
            logger.info("test_perfs = {}".format(self.test_perf))
            logger.info("test_probas = {}".format(self.test_probas))

            if content == "save_model":
                logger.info("\nSaving model...")
                cPickle.dump(self.model, open(self.model_fname, 'wb'))
                cPickle.dump(self.test_probas, open('probas_%s' % self.model_fname, 'wb'))
                logger.info("Model saved.")