from utils import object_utils

import DomainKnowledgeUser

class PostprocessingUnit(DomainKnowledgeUser.DomainKnowledgeUser):

    @classmethod
    def construct_postprocessing_unit(klass, description):
        output_index = description['output_index']
        modules = [object_utils.create_object(postprocessor_class) for postprocessor_class in description['modules']]

        return PostprocessingUnit(modules, output_index)

    def __init__(self, modules, output_index):
        super(PostprocessingUnit, self).__init__(modules)
        self.output_index = output_index

    def postprocess(self, data):
        return [postprocessor.postprocess(data) for postprocessor in self.modules]

    def get_output(self, postprocess_channels):
        return postprocess_channels[self.output_index]