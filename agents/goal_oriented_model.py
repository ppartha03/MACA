import abc

from system import system_modes
from agents.AbstractAgent import AbstractAgent

from TextData import TextData

class Slot(object):
    """
        A slot would contain one or multiple pieces of information that the system needs to ask.
    """
    def __init__(self, name, param_names = None, enabling_condition = lambda slots: True):
        super(Slot, self).__init__()
        self.enabling_condition = enabling_condition
        self.name = name

        if param_names is None: # The name of the parameter should be the same name with the slot
            self.param_names = [name]
        else:
            self.param_names = param_names

        self.values = {}
        for name in self.param_names:
            self.values[name] = None

    def clear(self):
        for name in self.values:
            self.values[name] = None

    def is_fully_filled(self):
        return all(value is not None for value in self.values.values())

    def get_value(self, param_name = None):
        if param_name is None:
            param_name = self.name

        assert param_name in self.values
        return self.values[param_name]

    def fill_value(self, value, param_name = None):
        if param_name is None:
            param_name = self.name

        assert param_name in self.values
        self.values[param_name] = value

    def __str__(self):
        return "Slot {} has name and values: {}".format(self.name, ', '.join(['{} --> {}'.format(name, value) for name, value in self.values.iteritems()]))


class IntentPolicy(object):
    """
        Policy to handle an intention of the user
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, slots):
        super(IntentPolicy, self).__init__()
        self.slots = {}
        for slot in slots:
            self.slots[slot.name] = slot

    def clear(self):
        for slot in self.slots.values():
            slot.clear()

    def get_unfinished_slots(self):
        return [slot for slot in self.slots.values() if slot.enabling_condition(self.slots) and not slot.is_fully_filled()]

    @abc.abstractmethod
    def get_info(self, sentence):
        """
            Extract all possible information and fill the slots.
            Return all unfilled or partially filled slots.
        """
        return self.get_unfinished_slots()

    @abc.abstractmethod
    def ask_info(self, unfilled_slots):
        pass

    def confirm_info(self):
        return "Please confirm the following information: {}.".format('; '.join([str(slot) for slot in self.slots.values()]))

    @abc.abstractmethod
    def get_confirmation(self, sentence):
        """
            Return True if yes, False if no.
        """
        pass

    @abc.abstractmethod
    def action_with_information(self):
        """
            Concrete action that the system will do once goal is achieved (all information collected).
        """
        pass

class GoalOrientedModel(AbstractAgent):
    """
        An abstract model for goal oriented models.
    """
    __metaclass__ = abc.ABCMeta

    STATE_UNIDENTIFIED_INTENT = 0
    STATE_IDENTIFIED_INTENT = 1
    STATE_CONFIRM_VALUES = 2

    def __init__(self, intents = [], domain_knowledge = None, mode = system_modes.EXECUTION):
        super(GoalOrientedModel, self).__init__(domain_knowledge, mode)

        self.state = GoalOrientedModel.STATE_UNIDENTIFIED_INTENT
        self.current_intent = None
        self.intents = intents

    @abc.abstractmethod
    def get_intent(self, sentence):
        """
            Attempt to extract the user intention from the given sentence.
            Return True if identified an intent, or False otherwise.
        """
        pass

    @abc.abstractmethod
    def ask_intent(self):
        """
            Return a question asking for user intention.
        """
        pass

    def _process_single_sentence(self, sentence):
        if self.state == GoalOrientedModel.STATE_UNIDENTIFIED_INTENT:
            if self.get_intent(sentence):
                self.state = GoalOrientedModel.STATE_IDENTIFIED_INTENT
                return self._process_single_sentence(sentence)
            else:
                return self.ask_intent()
        elif self.state == GoalOrientedModel.STATE_IDENTIFIED_INTENT:
            unfilled_slots = self.current_intent.get_info(sentence)
            if len(unfilled_slots) > 0:
                return self.current_intent.ask_info(unfilled_slots)
            else:
                self.state = GoalOrientedModel.STATE_CONFIRM_VALUES
                return self.current_intent.confirm_info()
        elif self.state == GoalOrientedModel.STATE_CONFIRM_VALUES:
            if self.current_intent.get_confirmation(sentence):
                result = self.current_intent.action_with_information()
                self.current_intent.clear()
                self.state = GoalOrientedModel.STATE_UNIDENTIFIED_INTENT
                return result
            else:
                self.state = GoalOrientedModel.STATE_IDENTIFIED_INTENT
                return ""

    def process_inputs(self, inputs):
        """
            Use the model preprocessing to provide this method with a list of sentences.
        """
        outputs = []
        for data in inputs:
            result = self._process_single_sentence(data)
            outputs.append(result)

        return outputs


    def model_postprocess(self, outputs):
        for data in outputs:
            self.queue_output(TextData(data))

    def process_notification(self, content, channel):
        logger.info("Agent received notification {0} on channel {1}.".format(content, channel))