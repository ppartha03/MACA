from utils import object_utils

class System(object):

    @classmethod
    def construct_system(klass, system_description):
        object_creator = object_utils.create_object

        input_device = object_creator(system_description['input'])
        output_device =  object_creator(system_description['output'])

        preprocessor = object_creator(system_description['preprocessing'])
        postprocessor = object_creator(system_description['postprocessing'])
        agent = object_creator(system_description['agent'])

        return System(input_device, output_device, preprocessor, postprocessor, agent)

    """
        System object holding all components of the system.
    """
    def __init__(self, input_device, output_device, preprocessor, postprocessor, agent):
        super(System, self).__init__()
        self.terminate = False

        self.input_device = input_device
        self.output_device = output_device
        self.preprocessor = preprocessor
        self.postprocessor = postprocessor

        self.agent = agent