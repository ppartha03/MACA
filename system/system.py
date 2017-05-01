import traceback

from utils.abstract_designs import PubSub
from utils import object_utils
object_creator = object_utils.create_object

import system_channels
import configuration_converter
from PreprocessingUnit import PreprocessingUnit
from PostprocessingUnit import PostprocessingUnit
from ListenerUnit import ListenerUnit


class System(PubSub.Publisher):

    @classmethod
    def construct_system(klass, system_description):
        system_description = configuration_converter.convert_to_latest_config(system_description)

        input_device = object_creator(system_description['input'])
        output_device =  object_creator(system_description['output'])

        preprocessing = PreprocessingUnit.construct_preprocessing_unit(system_description['preprocessing'])
        postprocessing = PostprocessingUnit.construct_postprocessing_unit(system_description['postprocessing'])
        listeners = ListenerUnit.construct_listener_unit(system_description['listeners'])

        # Initialize domain knowledge and dataset
        domain_knowledge = object_creator(system_description['domain_knowledge'])
        dataset = object_creator(system_description['dataset']) if 'dataset' in system_description else None
        if dataset:
            dataset.load_data()
        domain_knowledge.dataset = dataset

        if 'kwargs' not in system_description['agent']:
            system_description['agent']['kwargs'] = {}
        system_description['agent']['kwargs']['domain_knowledge'] = domain_knowledge # Make domain knowledge available at agent instantiation time
        agent = object_creator(system_description['agent'])

        preprocessing.set_domain_knowledge(domain_knowledge)
        postprocessing.set_domain_knowledge(domain_knowledge)

        output_system = System(input_device, output_device, preprocessing, postprocessing, listeners, agent, domain_knowledge)
        listeners.subscribe(input_device, (system_channels.INPUT, system_channels.SCORING))
        listeners.subscribe(output_system, (system_channels.INPUT, system_channels.OUTPUT))

        output_system.accept_subscription(agent, channels = (system_channels.TRAINING,))
        input_device.accept_subscription(agent, channels = (system_channels.TRAINING,))
        return output_system

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

    def _input_routine(self):
        """
            Return whether any input was processed.
        """
        raw_inputs = self.input_device.take_input()
        if not raw_inputs:
            return False

        self.publish(raw_inputs, channel = system_channels.INPUT)

        processed_inputs = [self.preprocessing.preprocess(data) for data in raw_inputs]
        self.agent.full_process(processed_inputs)

        return True

    def _output_routine(self):
        try:
            next_output = self.agent.next_output(timeout = self.runtime_config['output_queue_timeout'])
            if next_output:
                processed_outputs = self.postprocessing.postprocess(next_output)
                self.publish(processed_outputs, channel = system_channels.OUTPUT)

                to_write = self.postprocessing.get_output(processed_outputs)

                self.output_device.write_output(to_write)
        except: # Notify exception
            traceback.print_exc()

    def input_loop(self):
        while not self.terminate:
            self._input_routine()

    def output_loop(self):
        while not self.terminate:
            self._output_routine()

    def run(self):
        """
            Single loop implementation
        """
        while not self.terminate:
            self._input_routine()
            self._output_routine()