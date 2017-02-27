import argparse
import cPickle
import random
import copy
import numpy.random as np_rnd
from datetime import datetime
from apply_bpe import BPE


def string2indices(p_str, str_to_idx, bpe=None):
    """
    Lookup dictionary from word to index to retrieve the list of indices from a string of words.
    If bpe is present, will automatically convert regular string p_str to bpe formatted string.
    :param p_str: string of words corresponding to indices.
    :param str_to_idx: contains the mapping from words to indices.
    :param bpe: byte pair encoding object from apply_bpe.py
    :return: a new list of indices corresponding to the given string of words.
    """
    if bpe:
        bpe_string = bpe.segment(p_str.strip())  # convert from regular to bpe format
        return [str_to_idx[w] for w in bpe_string.split() if w in str_to_idx]
    else:
        return [str_to_idx[w] for w in p_str.strip().split() if w in str_to_idx]


def indices2string(p_indices, idx_to_str, bpe=None):
    """
    Lookup dictionary from word to index to retrieve the list of words from a list of indices.
    :param p_indices: list of indices corresponding to words.
    :param idx_to_str: contains the mapping from indices to words.
    :param bpe: byte pair encoding object from apply_bpe.py
    :return: a new string corresponding to the given list of indices.
    """
    if bpe:
        return ' '.join([idx_to_str[idx] for idx in p_indices if idx in idx_to_str]).replace(bpe.separator+' ', '')
    else:
        return ' '.join([idx_to_str[idx] for idx in p_indices if idx in idx_to_str])


def process_dialogues(dialogues):
    '''Removes </d> </s> at end, splits into contexts/ responses '''
    contexts = []
    responses = []
    for d in dialogues:
        d_proc = d[:-3]
        index_list = [i for i, j in enumerate(d_proc) if j == 1]
        split = index_list[-1] + 1
        context = filter(lambda idx: idx!=1, d_proc[:split])  # remove </s> from context
        contexts.append(context)
        response = filter(lambda idx: idx!=1, d_proc[split:])  # remove </s> from response
        responses.append(response)
    return contexts, responses


def main():
    parser = argparse.ArgumentParser()
    parser.register('type', 'bool', lambda v: v.lower() in ("yes", "true", "t", "1"))
    parser.add_argument('--data_dir', type=str, default='.', help='Input/Output directory to find original data and save new data')
    parser.add_argument('--inputs', nargs='+', type=str, required=True, help='File(s) of responses to be added')
    parser.add_argument('--data_fname', type=str, default='dataset_twitter_bpe.pkl', help='File name of new data')
    parser.add_argument('--data_embeddings', type=str, default='W_twitter_bpe.pkl', help='File name of new data embeddings')
    parser.add_argument('--random_model', type=bool, default=True, help='Flag to add a random retrieval model as part of the new data')
    parser.add_argument('--oversampling', type=bool, default=True, help='Flag to oversample true responses in order to have 50/50 true and false responses in the new data')
    args = parser.parse_args()
    print "args: ", args

    ###
    # Load the original Twitter dataset in BPE format - only TRUE responses
    ###
    print "\nLoading original twitter data..."
    dialogues = cPickle.load(open('%s/BPE/Train.dialogues.pkl' % args.data_dir, 'rb'))
    # get the list of contexts, and the list of TRUE responses.
    contexts, true_responses = process_dialogues(dialogues)

    ###
    # LOAD BPE DICTIONARIES: map bpe_indices/bpe_words - vocab ~ 5,000
    ###
    twitter_bpe = BPE(open('%s/BPE/Twitter_Codes_5000.txt' % args.data_dir, 'r').readlines())
    twitter_bpe_dict = cPickle.load(open('%s/BPE/Dataset.dict-5k.pkl' % args.data_dir, 'r'))
    twitter_bpe_str_to_idx = dict([(tok, tok_id) for tok, tok_id, _, _ in twitter_bpe_dict])
    twitter_bpe_idx_to_str = dict([(tok_id, tok) for tok, tok_id, _, _ in twitter_bpe_dict])
    print "BPE dictionary length: ", len(twitter_bpe_dict)

    print "original data loaded!"

    ###
    # LOAD GENERATED DATA
    ###
    model_responses = {}  # dictionary of the form {'model_id':[list of responses], ...}

    for response_file_name in args.inputs:
        print "\nProcessing ", response_file_name, "..."
        generated_data = open(response_file_name, 'rb')

        # Get the responses
        generated_str_responses = []
        for line in generated_data:
            line = line.replace(' </s>\n', '')
            generated_str_responses.append(line.replace('\n', ''))

        generated_bpe_responses = map(lambda r: string2indices(r, twitter_bpe_str_to_idx, twitter_bpe), generated_str_responses)

        assert(len(generated_bpe_responses) == len(contexts))
        model_responses[response_file_name] = generated_bpe_responses

        print "Finished processing file ", response_file_name

    ###
    # CREATE THE DATA SET
    ###
    print "\nCreating new dataset..."
    train_val_split_index = int(len(contexts) * 0.8)  # 80% training
    val_test_split_index = int(len(contexts) * 0.9)  # 10% validation 10% test
    print "number of samples =", len(contexts)
    print "train samples =", train_val_split_index
    print "val samples =", val_test_split_index - train_val_split_index
    print "test samples =", len(contexts) - val_test_split_index

    # Split the contexts into train/val/test
    train_contexts = contexts[:train_val_split_index]
    val_contexts = contexts[train_val_split_index:val_test_split_index]
    test_contexts = contexts[val_test_split_index:]
    # Split the true responses into train/val/test
    train_true_responses = true_responses[:train_val_split_index]
    val_true_responses = true_responses[train_val_split_index:val_test_split_index]
    test_true_responses = true_responses[val_test_split_index:]

    data = {
        'train': {'c': [], 'r': [], 'y': []},
        'val': {'c': [], 'r': [], 'y': [], 'id': []},
        'test': {'c': [], 'r': [], 'y': [], 'id': []},
    }

    # add TRUE responses to the data train, validation, and test sets.
    data['train']['c'].extend(train_contexts)
    data['train']['r'].extend(train_true_responses)
    data['train']['y'].extend([1] * len(train_true_responses))

    data['val']['c'].extend(val_contexts)
    data['val']['r'].extend(val_true_responses)
    data['val']['y'].extend([1] * len(val_true_responses))
    data['val']['id'].extend(['true'] * len(val_true_responses))

    data['test']['c'].extend(test_contexts)
    data['test']['r'].extend(test_true_responses)
    data['test']['y'].extend([1] * len(test_true_responses))
    data['test']['id'].extend(['true'] * len(test_true_responses))

    if args.random_model:
        # get the list of RANDOM responses.
        random_responses = copy.deepcopy(true_responses)
        random.shuffle(random_responses)
        assert len(contexts) == len(true_responses) == len(random_responses)

        # Split the random responses into train/val/test
        train_random_responses = random_responses[:train_val_split_index]
        val_random_responses = random_responses[train_val_split_index:val_test_split_index]
        test_random_responses = random_responses[val_test_split_index:]

        # add RANDOM responses to the data train, validation, and test sets.
        data['train']['c'].extend(train_contexts)
        data['train']['r'].extend(train_random_responses)
        data['train']['y'].extend([0] * len(train_random_responses))

        data['val']['c'].extend(val_contexts)
        data['val']['r'].extend(val_random_responses)
        data['val']['y'].extend([0] * len(val_random_responses))
        data['val']['id'].extend(['rand'] * len(val_random_responses))

        data['test']['c'].extend(test_contexts)
        data['test']['r'].extend(test_random_responses)
        data['test']['y'].extend([0] * len(test_random_responses))
        data['test']['id'].extend(['rand'] * len(test_random_responses))

    # add GENERATED responses.
    for model_name, generated_responses in model_responses.iteritems():
        # Split the generated responses into train/val/test
        train_generated_responses = generated_responses[:train_val_split_index]
        val_generated_responses = generated_responses[train_val_split_index:val_test_split_index]
        test_generated_responses = generated_responses[val_test_split_index:]

        # add GENERATED responses (and TRUE responses for the training set to have 50/50 true and false responses)
        data['train']['c'].extend(train_contexts)
        data['train']['r'].extend(train_generated_responses)
        data['train']['y'].extend([0] * len(train_generated_responses))

        data['val']['c'].extend(val_contexts)
        data['val']['r'].extend(val_generated_responses)
        data['val']['y'].extend([0] * len(val_generated_responses))
        data['val']['id'].extend([model_name] * len(val_generated_responses))

        data['test']['c'].extend(test_contexts)
        data['test']['r'].extend(test_generated_responses)
        data['test']['y'].extend([0] * len(test_generated_responses))
        data['test']['id'].extend([model_name] * len(test_generated_responses))

    if args.oversampling:
        # get the number of models with negative examples.
        false_response_models = len(model_responses)
        if args.random_model:
            false_response_models += 1

        # over sample by adding the same amount of true examples (-1 bcs already added true examples once)
        data['train']['c'].extend(train_contexts * (false_response_models-1))
        data['train']['r'].extend(train_true_responses * (false_response_models-1))
        data['train']['y'].extend([1] * len(train_true_responses) * (false_response_models-1))
        # making sure we have same amount of true and false responses.
        assert len(filter(lambda flag: flag==0, data['train']['y'])) == len(filter(lambda flag: flag==1, data['train']['y']))

    # Making sure each context has a unique response, flag (and model_id for val & test sets)
    assert len(data['train']['c']) == len(data['train']['r']) == len(data['train']['y'])
    assert len(data['val']['c']) == len(data['val']['r']) == len(data['val']['y']) == len(data['val']['id'])
    assert len(data['test']['c']) == len(data['test']['r']) == len(data['test']['y']) == len(data['test']['id'])

    print "New dataset created!"
    if args.random_model and args.oversampling:
        print 'New number of training examples: true+rand+(true+gen)*%d = %d' % (len(model_responses), len(data['train']['c']))
        print 'New number of validation examples: true+rand+gen*%d = %d' % (len(model_responses), len(data['val']['c']))
        print 'New number of testing examples: true+rand+gen*%d %d' % (len(model_responses), len(data['test']['c']))
    elif args.oversampling:
        print 'New number of training examples: true*%d+gen*%d = %d' % (len(model_responses), len(model_responses), len(data['train']['c']))
        print 'New number of validation examples: true+gen*%d = %d' % (len(model_responses), len(data['val']['c']))
        print 'New number of testing examples: true+gen*%d = %d' % (len(model_responses), len(data['test']['c']))
    elif args.random_model:
        print 'New number of training examples: true+rand+gen*%d = %d' % (len(model_responses), len(data['train']['c']))
        print 'New number of validation examples: true+rand+gen*%d = %d' % (len(model_responses), len(data['val']['c']))
        print 'New number of testing examples: true+rand+gen*%d %d' % (len(model_responses), len(data['test']['c']))
    else:
        print 'New number of training examples: true+gen*%d = %d' % (len(model_responses), len(data['train']['c']))
        print 'New number of validation examples: true+gen*%d = %d' % (len(model_responses), len(data['val']['c']))
        print 'New number of testing examples: true+gen*%d %d' % (len(model_responses), len(data['test']['c']))

    ###
    # SHUFFLE THE WHOLE TRAINING SET
    ###
    SEED = datetime.now()
    random.seed(SEED)
    random.shuffle(data['train']['c'])
    random.seed(SEED)
    random.shuffle(data['train']['r'])
    random.seed(SEED)
    random.shuffle(data['train']['y'])

    ###
    # SAVE THE RESULTING DATA
    # .pkl will have (data[train], data[val], data[test])
    ###
    print "\nSaving resulting dataset in %s/%s..." % (args.data_dir, args.data_fname)
    data_file = open("%s/%s" % (args.data_dir, args.data_fname), 'wb')
    cPickle.dump((data['train'], data['val'], data['test']), data_file, protocol=cPickle.HIGHEST_PROTOCOL)
    data_file.close()
    print "Saved."

    ###
    # SAVE RANDOM WORD EMBEDDINGS
    # .pkl will have (word embeddings, str_to_idx map)
    ###
    print "\nSaving random word embeddings in %s/%s..." % (args.data_dir, args.data_embeddings)
    vocab_size = len(twitter_bpe_dict)
    random_word_embeddings = np_rnd.random((vocab_size, 300))
    w_file = open("%s/%s" % (args.data_dir, args.data_embeddings), 'wb')
    cPickle.dump((random_word_embeddings, twitter_bpe_str_to_idx), w_file, protocol=cPickle.HIGHEST_PROTOCOL)
    w_file.close()
    print "Saved."


if __name__ == '__main__':
    main()
