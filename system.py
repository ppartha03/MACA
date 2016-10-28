from utils import object_utils

class System(object):

    @classmethod
    def construct_system(klass, system_description):
        object_creator = object_utils.create_object

        input_device = object_creator(system_description['input'])
        output_device =  object_creator(system_description['output'])

        preprocessors = [object_creator(preprocessor_description) for preprocessor_description in system_description['preprocessing']]
        postprocessors = [object_creator(postprocessor_description) for postprocessor_description in system_description['postprocessing']]
        agent = object_creator(system_description['agent'])

        domain_knowledge = object_creator(system_description['domain_knowledge'])
        for preprocessor in preprocessors:
            preprocessor.domain_knowledge = domain_knowledge

        for postprocessor in postprocessors:
            postprocessor.domain_knowledge = domain_knowledge

        agent.domain_knowledge = domain_knowledge

        return System(input_device, output_device, preprocessors, postprocessors, agent, domain_knowledge)

    """
        System object holding all components of the system.
    """
    def __init__(self, input_device, output_device, preprocessors, postprocessors, agent, domain_knowledge):
        super(System, self).__init__()
        self.terminate = False

        self.input_device = input_device
        self.output_device = output_device
        self.preprocessors = preprocessors
        self.postprocessors = postprocessors

        self.agent = agent
        self.domain_knowledge = domain_knowledge