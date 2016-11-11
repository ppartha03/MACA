import abc
import Queue

from utils.abstract_designs import PubSub

class AbstractAgent(PubSub.Subscriber):
    """
        AbstractAgent: represent an abstract agent with internal information state.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(AbstractAgent, self).__init__()
        self.output_data = Queue.Queue() # Synchronized blocking queue to stored pending output.

    @abc.abstractmethod
    def process_inputs(self, inputs):
        """
            Process user text inputs.

            Parameters
            ----------
            inputs : a list of TextData objects.

            Returns
            -------
            None
        """
        pass


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

    def process_notification(self, content, tag):
        """
            Override this to process any feedback information.
        """
        pass