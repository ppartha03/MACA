#!/usr/bin/env python

import argparse
import cPickle
import traceback
import logging
import time
import sys

import os
import numpy
import codecs
import search
import utils

from dialog_encdec import DialogEncoderDecoder
from numpy_compat import argpartition
from state import prototype_ubuntu_HRED #state

logger = logging.getLogger(__name__)

class Timer(object):
    def __init__(self):
        self.total = 0

    def start(self):
        self.start_time = time.time()

    def finish(self):
        self.total += time.time() - self.start_time

def parse_args():
    parser = argparse.ArgumentParser("Sample (with beam-search) from the session model")

    parser.add_argument("--ignore-unk",
            action="store_false",
            help="Allows generation procedure to output unknown words (<unk> tokens)")

    parser.add_argument("model_prefix",
            help="Path to the model prefix (without _model.npz or _state.pkl)")

#    parser.add_argument("context",
#            help="File of input contexts")

#    parser.add_argument("output",
#            help="Output file")
    
    parser.add_argument("--beam_search",
                        action="store_true",
                        help="Use beam search instead of random search")

    parser.add_argument("--n-samples",
            default="1", type=int,
            help="Number of samples")

    parser.add_argument("--n-turns",
                        default=1, type=int,
                        help="Number of dialog turns to generate")

    parser.add_argument("--verbose",
            action="store_true", default=False,
            help="Be verbose")

    parser.add_argument("changes", nargs="?", default="", help="Changes to state")
    return parser.parse_args()

def main():
    args = parse_args()
    state = prototype_ubuntu_HRED()#state()

    state_path = args.model_prefix + "_state.pkl"
    model_path = args.model_prefix + "_model.npz"

    with open(state_path) as src:
        state.update(cPickle.load(src))

    state['dictionary'] = "/home/ml/rlowe1/UbuntuData/Dataset.dict.pkl"

    logging.basicConfig(level=getattr(logging, state['level']), format="%(asctime)s: %(name)s: %(levelname)s: %(message)s")

    model = DialogEncoderDecoder(state) 
    
    sampler = search.RandomSampler(model)
    if args.beam_search:
        sampler = search.BeamSampler(model)

    if os.path.isfile(model_path):
        logger.debug("Loading previous model")
        model.load(model_path)
    else:
        raise Exception("Must specify a valid model path")
  
    # Start chat loop
    utterances = collections.deque()
    
    while (True):
       var = raw_input("User - ")

       # Increase number of utterances. We just set it to zero for simplicity so that model has no memory. 
       # But it works fine if we increase this number
       while len(utterances) > 0:
           utterances.popleft()
         
       current_utterance = [ model.end_sym_utterance ] + ['<first_speaker>'] + var.split() + [ model.end_sym_utterance ]
       utterances.append(current_utterance)
         
       #TODO Sample a random reply. To spice it up, we could pick the longest reply or the reply with the fewest placeholders...
       seqs = list(itertools.chain(*utterances))

       #TODO Retrieve only replies which are generated for second speaker...
       sentences = sample(model, \
            seqs=[seqs], ignore_unk=args.ignore_unk, \
            sampler=sampler, n_samples=5)

       if len(sentences) == 0:
           raise ValueError("Generation error, no sentences were produced!")

       utterances.append(sentences[0][0].split())

       reply = sentences[0][0].encode('utf-8')
       print "AI - ", remove_speaker_tokens(reply)
  
#    contexts = [[]]
#    lines = open(args.context, "r").readlines()
#    if len(lines):
#        contexts = [x.strip() for x in lines]
    
#    print('Sampling started...')
#    context_samples, context_costs = sampler.sample(contexts,
#                                            n_samples=args.n_samples,
#                                            n_turns=args.n_turns,
#                                            ignore_unk=args.ignore_unk,
#                                            verbose=args.verbose)
#    print('Sampling finished.')
#    print('Saving to file...')
     
    # Write to output file
#    output_handle = open(args.output, "w")
#    for context_sample in context_samples:
#        print >> output_handle, '\t'.join(context_sample)
#    output_handle.close()
#    print('Saving to file finished.')
#    print('All done!')

if __name__ == "__main__":
    main()

