from utils import object_utils
import DomainKnowledgeUser


class PreprocessingUnit(DomainKnowledgeUser.DomainKnowledgeUser):

    @classmethod
    def construct_preprocessing_unit(klass, description):
        modules = [object_utils.create_object(preprocessor_class) for preprocessor_class in description]
        return PreprocessingUnit(modules)

    def __init__(self, modules):
        super(PreprocessingUnit, self).__init__(modules)

    def preprocess(self, data):
        return [preprocessor.preprocess(data) for preprocessor in self.modules]