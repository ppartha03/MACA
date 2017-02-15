import abc

import numpy as np

from AbstractDomainKnowledge import AbstractDomainKnowledge

class AbstractPOMDPDomainKnowledge(AbstractDomainKnowledge):

    __metaclass__ = abc.ABCMeta

    """
        Template for a pomdp domain knowledge.
    """
    def __init__(self):
        super(AbstractPOMDPDomainKnowledge, self).__init__()

        self.states = tuple()
        self.actions = tuple()
        self.observations = tuple()

    def get_states(self):
        """
            Return a tuple of states, can be of any data type.
        """
        return self.states

    def get_actions(self):
        """
            Return a tuple of actions, can be of any data type.
        """
        return self.actions

    def get_observations(self):
        """
            Return a tuple of observations, can be of any data type.
        """
        return self.observations

class VoiceMailPomdpDomainKnowledge(AbstractPOMDPDomainKnowledge):

    """
        Sample implementation of a pomdp domain knowledge.
    """
    def __init__(self):
        super(VoiceMailPomdpDomainKnowledge, self).__init__()

        self.states = ('save', 'delete')
        self.actions = ('ask', 'doSave', 'doDelete')
        self.observations = ('hearSave', 'hearDelete')

