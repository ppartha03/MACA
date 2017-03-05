import abc
import Queue

from utils.abstract_designs import PubSub
from system import system_modes

class AbstractAgent(PubSub.Subscriber):
    """
        AbstractAgent: represent an abstract agent with internal information state.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, domain_knowledge = None, mode = system_modes.EXECUTION):
        super(AbstractAgent, self).__init__()
        self.output_data = Queue.Queue() # Synchronized blocking queue to stored pending output.
        self.domain_knowledge = domain_knowledge
        self.mode = mode

    def model_preprocess(self, inputs):
        """
            Internal preprocessing of the models. Output of this will be passed on to the main internal processing of the model.
            Override if need be to perform any required internal preprocessing.

            Parameters
            ----------
            inputs : a list of TextData objects.

            Returns
            -------
            Appropriate outputs to pass on to the main internal processing. Alternatively this can modify model's internal state.
        """
        return inputs

    @abc.abstractmethod
    def model_postprocess(self, outputs):
        """
            Internal postprocessing of the models. Output of this will be passed on to postprocessing unit of the system.
            Override to need be to perform any required internal postprocessing.

            After this method finishes, appropriate outputs MUST be put onto the output queue, ready for the system postprocessing module.
            Use method queue_output avaialble in this class to enqueue the output.

            Parameters
            ----------
            inputs : output of the main internal processing of the model.

            Returns
            -------
            None. Output of appropriate formats are put onto the output queue.

        """
        pass

    @abc.abstractmethod
    def process_inputs(self, inputs):
        """
            Process user inputs. This is the main internal processing of the model. Data must have been preprocessed internally
            before coming to this method.

            Parameters
            ----------
            inputs : data from model internal preprocessing.

            Returns
            -------
            Appropriate output for model internal postprocessing.
        """
        pass

    def full_process(self, inputs):
        """
            Full processing pipeline of the model. This includes preprocessing, main internal processing and postprocessing.
            This method MUST NOT be overriden.

            Parameters
            ----------
            inputs : data from system preprocessing.

            Returns
            -------
            Output from model internal postprocess.
        """
        preprocessed = self.model_preprocess(inputs)
        raw_response = self.process_inputs(preprocessed)
        return self.model_postprocess(raw_response)


    def next_output(self, timeout = None):
        """
            Get the next available output from this agent with timeout.
            THe implementation must implement blocking wait until an output is available, or timeout happens.

            Parameters
            ----------
            timeout : timeout in seconds, or None for infinite timeout

            Returns
            -------
            The next available output from the agent, or None if timeout.
        """
        try:
            return self.output_data.get(True, timeout = timeout)
        except Queue.Empty:
            return None

    def queue_output(self, data):
        """
            Enqueue this data as an available output.
        """
        self.output_data.put(data)

    def process_notification(self, content, channel):
        """
            Override this to process any feedback information.
        """
        pass