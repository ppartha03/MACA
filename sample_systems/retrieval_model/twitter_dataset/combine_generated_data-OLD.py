import argparse
import cPickle
import random
import numpy as np
from datetime import datetime
from apply_bpe import BPE


def revertDictionary(p_dict):
    """
    Create a new dictionary that maps values to keys.
    :param p_dict: the original dictionary that maps keys to values.
    :return: new dictionary that maps values to keys.
    """
    out = {}
    for key, value in p_dict.iteritems():
        out[value] = key
    return out


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
        return ' '.join([idx_to_str[idx] for idx in p_indices if idx in idx_to_str]).replace(bpe.separator + ' ', '')
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
        contexts.append(d_proc[:split])
        responses.append(d_proc[split:] + [1])
    return contexts, responses


def getIndex(context, data):
    """
    Search for the set (train or val or test set) where context is present.
    :param context: array of numbers representing the context that we are looking for.
    :param data: dictionary that has all the training, validation, test sets.
    :return: 'train' or 'val' or 'test' according to which set the context is found in or '' if not found.
    """
    if context in data['test']['c']:
        return "test"
    elif context in data['val']['c']:
        return "val"
    elif context in data['train']['c']:
        return "train"
    return ""


def remove_token(data, token):
    """
    Remove a specific token from the data. If one data item become empty, remove it.
    :param data: dictionary of this form {'c':[[#,...,#], ...], 'r':[[#,...,#], ...], 'y':[#,...,#]}
    :param token: token to be removed from all context and responses in the data.
    :return: a clean version of the data.
    """
    clean_data = {'c': [], 'r': [], 'y': []}
    for i, (context, response) in enumerate(zip(data['c'], data['r'])):  # for each context, response filter out 'token'
        new_context = filter(lambda idx: idx != token, context)
        if len(new_context) <= 0:
            continue  # skip this context/response/flag instance.
        new_response = filter(lambda idx: idx != token, response)
        if len(new_response) <= 0:
            continue  # skip this context/response/flag instance.
        clean_data['c'].append(new_context)
        clean_data['r'].append(new_response)
        clean_data['y'].append(data['y'][i])
    return clean_data


def main():
    parser = argparse.ArgumentParser()
    parser.register('type', 'bool', lambda v: v.lower() in ("yes", "true", "t", "1"))
    parser.add_argument('--data_dir', type=str, default='.', help='Input dir')
    parser.add_argument('--inputs', nargs='+', type=str, required=True, help='File(s) of responses to be added')
    parser.add_argument('--save_data', type='bool', default=True, help='Whether to save the new data')
    parser.add_argument('--data_fname', type=str, default='dataset_twitter_bpe_indices.pkl',
                        help='Destination of new data')
    args = parser.parse_args()
    print "args: ", args

    ###
    # Load the current training, validation, test sets of Twitter
    # Load the DE dictionaries: map words to indices - vocab ~ 200,000
    ###
    print "\nLoading original twitter data..."
    # train_data, val_data, test_data = cPickle.load(open('%s/DE/dataset_twitter_de.pkl' % args.data_dir, 'rb'))
    # _, twitter_de_str_to_idx = cPickle.load(open('%s/DE/W_twitter.pkl' % args.data_dir, 'rb'))
    # twitter_de_idx_to_str = revertDictionary(twitter_de_str_to_idx)
    # print "DE dictionary length =", len(twitter_de_str_to_idx)

    ###
    # Load the original Twitter dataset in BPE format - only TRUE responses
    ###
    train_dialogues = cPickle.load(open('%s/BPE/Train.dialogues.pkl' % args.data_dir, 'rb'))
    val_dialogues = cPickle.load(open('%s/BPE/Valid.dialogues.pkl' % args.data_dir, 'rb'))
    test_dialogues = cPickle.load(open('%s/BPE/Test.dialogues.pkl' % args.data_dir, 'rb'))


    train_data = {'c': [], 'r': [], 'y': []}
    train_contexts, train_responses = process_dialogues(train_dialogues)
    for train_context, train_response in zip(train_contexts, train_responses):
        train_data['c'].append(train_context)
        train_data['r'].append(train_response)
        train_data['y'].append(1)
    val_data = {'c':[], 'r':[], 'y':[]}
    val_contexts, val_responses = process_dialogues(val_dialogues)
    for val_context, val_response in zip(val_contexts, val_responses):
        if val_context in train_contexts:
            continue  # skip this item if its context is already in training set.
        val_data['c'].append(val_context)
        val_data['r'].append(val_response)
        val_data['y'].append(1)
    test_data = {'c':[], 'r':[], 'y':[]}
    test_contexts, test_responses = process_dialogues(test_dialogues)
    for test_context, test_response in zip(test_contexts, test_responses):
        if test_context in train_contexts:
            continue  # skip this item if its context is already in training set.
        test_data['c'].append(test_context)
        test_data['r'].append(test_response)
        test_data['y'].append(1)

    # print "making sure filtering is valid for CONTEXTS..."
    # for c in train_data['c']:
    #     assert c not in val_data['c']
    #     assert c not in test_data['c']
    # print "ok"

    ###
    # LOAD BPE DICTIONARIES: map bpe_indices/bpe_words - vocab ~ 5,000
    ###
    twitter_bpe = BPE(open('%s/BPE/Twitter_Codes_5000.txt' % args.data_dir, 'r').readlines())
    twitter_bpe_dict = cPickle.load(open('%s/BPE/Dataset.dict-5k.pkl' % args.data_dir, 'r'))
    twitter_bpe_str_to_idx = dict([(tok, tok_id) for tok, tok_id, _, _ in twitter_bpe_dict])
    twitter_bpe_idx_to_str = dict([(tok_id, tok) for tok, tok_id, _, _ in twitter_bpe_dict])
    print "BPE dictionary length: ", len(twitter_bpe_dict)
    print 'Number of training examples: %d' % (len(train_data['c']))
    print 'Number of validation examples: %d' % (len(val_data['c']))
    print 'Number of testing examples: %d' % (len(test_data['c']))
    print "data loaded!"

    ###
    # Remove **unknown** tokens & delete empty context / responses
    ###
    # print "\nRemoving **unknown** tokens and empty context or responses..."
    # train_data = remove_token(train_data, 172123)
    # val_data = remove_token(val_data, 172123)
    # test_data = remove_token(test_data, 172123)
    # print "done."
    # print 'Number of training examples: %d' % (len(train_data['c']))
    # print 'Number of validation examples: %d' % (len(val_data['c']))
    # print 'Number of testing examples: %d' % (len(test_data['c']))

    data = {'train': train_data, 'val': val_data, 'test': test_data}

    # for i in range(15):
    #     print "data[train][c][",i,"] =", data['train']['c'][i]
    #     print " =", indices2string(data['train']['c'][i], twitter_bpe_idx_to_str, twitter_bpe)
    #     print "data[train][r][",i,"] =", data['train']['r'][i]
    #     print " =", indices2string(data['train']['r'][i], twitter_bpe_idx_to_str, twitter_bpe)
    #     print "data[train][y][",i,"] =", data['train']['y'][i]
    #     print "- - -"
    # print "data[val][c][0] =", data['val']['c'][0]
    # print " =", indices2string(data['val']['c'][0], twitter_bpe_idx_to_str, twitter_bpe)
    # print "data[val][r][0] =", data['val']['r'][0]
    # print " =", indices2string(data['val']['r'][0], twitter_bpe_idx_to_str, twitter_bpe)
    # print "data[val][y][0] =", data['val']['y'][0]
    # print "- - -"
    # print "data[test][c][0] =", data['test']['c'][0]
    # print " =", indices2string(data['test']['c'][0], twitter_bpe_idx_to_str, twitter_bpe)
    # print "data[test][r][0] =", data['test']['r'][0]
    # print " =", indices2string(data['test']['r'][0], twitter_bpe_idx_to_str, twitter_bpe)
    # print "data[test][y][0] =", data['test']['y'][0]
    # print "- - -"

    ###
    # CONVERT D.E. LIST OF INDICES TO BPE LIST OF INDICES
    ###
    # bpe_indices = {
    #     'train': {'c': [], 'r': [], 'y': data['train']['y']},
    #     'val': {'c': [], 'r': [], 'y': data['val']['y']},
    #     'test': {'c': [], 'r': [], 'y': data['test']['y']},
    # }
    # print "\nConverting data to bpe indices..."
    # for key, dialog in data.iteritems():
    #     # key = 'train' or 'val' or 'test'
    #     # dialog = {'c':[], 'r':[], 'y':[]}
    #     for context, response in zip(dialog['c'], dialog['r']):
    #         # print "DE indices (context) =", context
    #         # print "DE indices (response) =", response
    #         # Convert from list of indices to regular string.
    #         string_context = indices2string(context, twitter_de_idx_to_str)
    #         string_response = indices2string(response, twitter_de_idx_to_str)
    #         # print "DE string (context) =", string_context
    #         # print "DE string (response)", string_response
    #         # Convert from regular string to bpe string and bpe indices.
    #         bpe_indices_context = string2indices(string_context, twitter_bpe_str_to_idx, twitter_bpe)
    #         bpe_indices_response = string2indices(string_response, twitter_bpe_str_to_idx, twitter_bpe)
    #         # print "BPE string (context) =", indices2string(bpe_indices_context, twitter_bpe_idx_to_str, twitter_bpe)
    #         # print "BPE string (response) =", indices2string(bpe_indices_response, twitter_bpe_idx_to_str, twitter_bpe)
    #         # print "BPE indices (context) =", bpe_indices_context
    #         # print "BPE indices (response) =", bpe_indices_response
    #         # print "y =", dialog['y'][:15]
    #         # print ""
    #         bpe_indices[key]['c'].append(bpe_indices_context)
    #         bpe_indices[key]['r'].append(bpe_indices_response)
    # data = bpe_indices
    # print "train", len(data['train']['c'])
    # print "val", len(data['val']['c'])
    # print "test", len(data['test']['c'])
    # print "data converted!"

    # for i in range(15):
    #     print "data[train][c][",i,"] =", data['train']['c'][i]
    #     print " =", indices2string(data['train']['c'][i], twitter_bpe_idx_to_str, twitter_bpe)
    #     print "data[train][r][",i,"] =", data['train']['r'][i]
    #     print " =", indices2string(data['train']['r'][i], twitter_bpe_idx_to_str, twitter_bpe)
    #     print "data[train][y][",i,"] =", data['train']['y'][i]
    #     print "- - -"
    # print "data[val][c][0] =", data['val']['c'][0]
    # print " =", indices2string(data['val']['c'][0], twitter_bpe_idx_to_str, twitter_bpe)
    # print "data[val][r][0] =", data['val']['r'][0]
    # print " =", indices2string(data['val']['r'][0], twitter_bpe_idx_to_str, twitter_bpe)
    # print "data[val][y][0] =", data['val']['y'][0]
    # print "- - -"
    # print "data[test][c][0] =", data['test']['c'][0]
    # print " =", indices2string(data['test']['c'][0], twitter_bpe_idx_to_str, twitter_bpe)
    # print "data[test][r][0] =", data['test']['r'][0]
    # print " =", indices2string(data['test']['r'][0], twitter_bpe_idx_to_str, twitter_bpe)
    # print "data[test][y][0] =", data['test']['y'][0]
    # print "- - -"

    ### Making sure no train dialogues is present in test or validation sets:
    # print "\nmaking sure no train_context is in test or validation set..."
    # for train_c in data['train']['c']:
    #     assert train_c not in data['test']['c']
    #     assert train_c not in data['val']['c']
    # print "ok."

    ###
    # LOAD GENERATED DATA & ADD IT TO CURRENT DATA
    ###
    for response_file_name in args.inputs:
        print "\nProcessing ", response_file_name, "..."
        added_in_train = 0
        added_in_val = 0
        added_in_test = 0
        generated_data = open(response_file_name, 'rb')

        # Get the responses
        generated_str_responses = []
        for line in generated_data:
            generated_str_responses.append(line.replace('\n', ''))

        generated_bpe_responses = map(lambda r: string2indices(r, twitter_bpe_str_to_idx, twitter_bpe),
                                      generated_str_responses)

        assert (len(generated_bpe_responses) == len(train_contexts))

        # Print the first few context/responses to check if some makes sense
        # for i in range(15):
        #     print train_bpe_contexts[i]
        #     print ' =', train_str_contexts[i]
        #     print generated_str_responses[i]
        #     print ""

        for context, response in zip(train_contexts, generated_bpe_responses):
            # dict_index = 'train'
            dict_index = getIndex(context, data)  # get the set in which that context is present (train, val, test)
            if len(dict_index) <= 0:  # if not found, error
                print context, "not found."
                print "ERROR:", indices2string(context, twitter_bpe_idx_to_str, twitter_bpe), "not found.\n"
                continue  # skip the following lines: don't add this instance to the data
            if len(dict_index) < 5:
                print "WARNING: train context found in ", dict_index
                # print context
                # print indices2string(context, twitter_bpe_idx_to_str, twitter_bpe), "\n"
            data[dict_index]['c'].append(context)
            data[dict_index]['r'].append(response)
            data[dict_index]['y'].append(0)
            if dict_index == 'train':
                added_in_train += 1
            elif dict_index == 'val':
                added_in_val += 1
            elif dict_index == 'test':
                added_in_test += 1
            else:
                print "added instance to wrong set: ", dict_index

        print "Finished processing file ", response_file_name
        print "Added", added_in_train, "instances in train,", added_in_val, "instances in validation,", added_in_test, "instances in test set."
        print 'New number of training examples: %d' % (len(train_data['c']))
        print 'New number of validation examples: %d' % (len(val_data['c']))
        print 'New number of testing examples: %d' % (len(test_data['c']))

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
    ###
    if args.save_data:
        print "\nSaving resulting dataset in ", args.data_fname, "..."
        file = open(args.data_fname, 'wb')
        cPickle.dump((data['train'], data['val'], data['test']), file, protocol=cPickle.HIGHEST_PROTOCOL)
        file.close()
        print "Saved."

if __name__ == '__main__':
    main()
