import traceback

from utils import object_utils
object_creator = object_utils.create_object

from PreprocessingUnit import PreprocessingUnit
from PostprocessingUnit import PostprocessingUnit
from ListenerUnit import ListenerUnit


class System(object):

    @classmethod
    def construct_system(klass, system_description):
        input_device = object_creator(system_description['input'])
        output_device =  object_creator(system_description['output'])

        preprocessing = PreprocessingUnit.construct_preprocessing_unit(system_description['preprocessing'])
        postprocessing = PostprocessingUnit.construct_postprocessing_unit(system_description['postprocessing'])
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

    def configure(self, config):
        """
            Configure the runtime parameters of the system. Architectural parameters must be specified in the system description and
            parsed at system construction time.
        """
        self.runtime_config = config

    def input_loop(self):
        while not self.terminate:
            raw_inputs = self.input_device.take_input()
            self.listeners.listen_to_inputs(raw_inputs)

            processed_inputs = [self.preprocessing.preprocess(data) for data in raw_inputs]
            self.agent.process_inputs(processed_inputs)

    def output_loop(self):
        while not self.terminate:
            try:
                next_output = self.agent.next_output(timeout = self.runtime_config['io_timeout'])
                if next_output:
                    processed_outputs = self.postprocessing.postprocess(next_output)
                    self.listeners.listen_to_output(processed_outputs)

                    to_write = self.postprocessing.get_output(processed_outputs)

                    self.output_device.write_output(to_write)
            except: # Notify exception
                traceback.print_exc()