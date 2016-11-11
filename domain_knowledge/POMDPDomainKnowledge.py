import abc

import numpy as np

from AbstractDomainKnowledge import AbstractDomainKnowledge

class POMDPDomainKnowledge(AbstractDomainKnowledge):

	__metaclass__ = abc.ABCMeta

	"""
		Template for a pomdp domain knowledge.
	"""
	def __init__(self):
		super(POMDPDomainKnowledge, self).__init__()

		self.states = tuple()
		self.actions = tuple()
		self.observations = tuple()

	def get_states(self):
		"""
			Return a tuple of states, can be of any data type.
		"""
		return self.states

	@abc.abstractmethod
	def get_actions(self):
		"""
			Return a tuple of actions, can be of any data type.
		"""
		return self.actions

	@abc.abstractmethod
	def get_observations(self):
		"""
			Return a tuple of observations, can be of any data type.
		"""
		return self.observations

	@abc.abstractmethod
	def get_transition_probability(self, action_taken):
		"""
			Return a numpy matrix whose rows are start state, columns are end state and values are
			the transition probability P(<next-state> | <start-state>, <action>).

			States, observations and actions are specified in the same order specified in other get methods of this class.
		"""
		pass

	@abc.abstractmethod
	def get_observation_probability(self, action):
		"""
			Return a matrix whose rows are next-states, columns are observations, and values are
			P(<obs> | <action>, <next-state>)

			States, observations and actions are specified in the same order specified in other get methods of this class.
		"""
		pass

	@abc.abstractmethod
	def get_rewards(self, action, start_state):
		"""
			Return a matrix whose rows are next-state, columns are observations and values are rewards.

			States, observations and actions are specified in the same order specified in other get methods of this class.
		"""
		pass



class SamplePomdpDomainKnowledge(POMDPDomainKnowledge):

	"""
		Sample implementation of a pomdp domain knowledge.
	"""
	def __init__(self):
		super(SamplePomdpDomainKnowledge, self).__init__()

		self.states = ('heavy', 'light', 'novel')
		self.actions = ('ask', 'sayHeavy', 'sayLight', 'sayNovel')
		self.observations = ('hearHeavy', 'hearLight', 'hearNovel')

	def get_transition_probability(self, action_taken):
		if action_taken == 'ask':
			return np.eye(len(self.states), len(self.states))
		else:
			return np.array([
				[0.4, 0.4, 0.2],
				[0.4, 0.4, 0.2],
				[0.4, 0.4, 0.2]
				])

	def get_observation_probability(self, action):
		if action_taken == 'ask':
			return np.array([
				[0.7 0.01 0.29],
				[0.01 0.7 0.29],
				[0.1 0.1 0.8]
				])

		else:
			return np.array([
				[1.0/3, 1.0/3, 1.0/3],
				[1.0/3, 1.0/3, 1.0/3],
				[1.0/3, 1.0/3, 1.0/3],
				])

	def get_rewards(self, action, start_state):
		if action == 'ask':
			return np.ones((3, 3), dtype = np.intc) * 5
		else:
			values = {
				'sayHeavy' : {
					'heavy' : 5,
					'light' : -10,
					'novel' : -2
				},
				'sayLight' : {
					'heavy' : 5,
					'light' : -10,
					'novel' : -2
				},
				'sayNovel' : {
					'heavy' : 5,
					'light' : -2,
					'novel' : 2
				},
			}

			return np.ones((3, 3), dtype = np.intc) * values[action][start_state]