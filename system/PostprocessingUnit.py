from utils import object_utils

import DomainKnowledgeUser

class PostprocessingUnit(DomainKnowledgeUser.DomainKnowledgeUser):

    @classmethod
    def construct_postprocessing_unit(klass, description):
        output_index = description['output_index']
        modules = [object_utils.create_object(postprocessor_class) for postprocessor_class in description['modules']]
        is_parallel = description.get('parallel', True)

        return PostprocessingUnit(modules, output_index, is_parallel)

    def __init__(self, modules, output_index, parallel = True):
        super(PostprocessingUnit, self).__init__(modules)
        self.output_index = output_index
        self.parallel = parallel

    def postprocess(self, data):
        if self.parallel:
            return [postprocessor.postprocess(data) for postprocessor in self.modules]
        else: # Sequential
            output = data
            for postprocessor in self.modules:
                output = postprocessor.postprocess(output)

            return [output]


    def get_output(self, postprocess_channels):
        return postprocess_channels[self.output_index]