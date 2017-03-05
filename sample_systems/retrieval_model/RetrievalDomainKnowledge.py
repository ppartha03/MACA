import cPickle

from domain_knowledge import AbstractDomainKnowledge


class RetrievalTwitterDataset(AbstractDomainKnowledge.AbstractDataset):
    def __init__(self, input_dir, dataset_fname):
        super(RetrievalTwitterDataset, self).__init__()
        self.input_dir = input_dir
        self.dataset_fname = dataset_fname


    def load_data(self):
        self.train_data, self.val_data, self.test_data = cPickle.load(open('%s/%s' % (self.input_dir, self.dataset_fname), 'rb'))

    def get_training_data(self):
        return self.train_data

    def get_validation_data(self):
        return self.val_data

    def get_testing_data(self):
        return self.test_data