from utils import object_utils

object_creator = object_utils.create_object

class DomainKnowledgeUser(object):
    def __init__(self, modules):
        super(DomainKnowledgeUser, self).__init__()
        self.modules = modules

    def set_domain_knowledge(self, domain_knowledge):
        for module in self.modules:
            self.domain_knowledge = domain_knowledge

class PreprocessingUnit(DomainKnowledgeUser):

    @classmethod
    def construct_preprocessing_unit(klass, description):
        modules = [object_creator(preprocessor_class) for preprocessor_class in description]
        return PreprocessingUnit(modules)

    def __init__(self, modules):
        super(PreprocessingUnit, self).__init__(modules)

    def preprocess(self, data):
        return [preprocessor.preprocess(data) for preprocessor in self.modules]

class PostProcessingUnit(DomainKnowledgeUser):

    @classmethod
    def construct_postprocessing_unit(klass, description):
        output_index = description['output_index']
        modules = [object_creator(postprocessor_class) for postprocessor_class in description['modules']]

        return PostProcessingUnit(modules, output_index)

    def __init__(self, modules, output_index):
        super(PostProcessingUnit, self).__init__(modules)
        self.output_index = output_index

    def postprocess(self, data):
        return [postprocessor.postprocess(data) for postprocessor in self.modules]

    def get_output(self, postprocess_channels):
        return postprocess_channels[self.output_index]

class ListenerUnit(DomainKnowledgeUser):

    @classmethod
    def construct_listener_unit(klass, description):
        modules = [object_creator(listener_class) for listener_class in description]
        return ListenerUnit(modules)

    def __init__(self, modules):
        super(ListenerUnit, self).__init__(modules)

    def listen_to_inputs(self, inputs):
        for data in inputs:
            for module in self.modules:
                module.listen_to_input(data)

    def listen_to_output(self, postprocess_channels):
        for module in self.modules:
            module.listen_to_output(postprocess_channels)


class System(object):

    @classmethod
    def construct_system(klass, system_description):
        input_device = object_creator(system_description['input'])
        output_device =  object_creator(system_description['output'])

        preprocessing = PreprocessingUnit.construct_preprocessing_unit(system_description['preprocessing'])
        postprocessing = PostProcessingUnit.construct_postprocessing_unit(system_description['postprocessing'])
        listeners = ListenerUnit.construct_listener_unit(system_description['listeners'])

        agent = object_creator(system_description['agent'])

        domain_knowledge = object_creator(system_description['domain_knowledge'])

        preprocessing.set_domain_knowledge(domain_knowledge)
        postprocessing.set_domain_knowledge(domain_knowledge)

        agent.domain_knowledge = domain_knowledge

        return System(input_device, output_device, preprocessing, postprocessing, listeners, agent, domain_knowledge)

    """
        System object holding all components of the system.
    """
    def __init__(self, input_device, output_device, preprocessing, postprocessing, listeners, agent, domain_knowledge):
        super(System, self).__init__()
        self.terminate = False

        self.input_device = input_device
        self.output_device = output_device

        self.preprocessing = preprocessing
        self.postprocessing = postprocessing
        self.listeners = listeners

        self.agent = agent
        self.domain_knowledge = domain_knowledge