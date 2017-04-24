from utils import object_utils
import DomainKnowledgeUser


class PreprocessingUnit(DomainKnowledgeUser.DomainKnowledgeUser):

    @classmethod
    def construct_preprocessing_unit(klass, description):
        modules = [object_utils.create_object(preprocessor_class) for preprocessor_class in description['modules']]
        is_parallel = description.get('parallel', True)

        return PreprocessingUnit(modules, is_parallel)

    def __init__(self, modules, parallel = True):
        super(PreprocessingUnit, self).__init__(modules)
        self.parallel = parallel

    def preprocess(self, data):
        if self.parallel:
            return [preprocessor.preprocess(data) for preprocessor in self.modules]
        else: # Sequential
            output = data
            for preprocessor in self.modules:
                output = preprocessor.preprocess(output)

            return [output]