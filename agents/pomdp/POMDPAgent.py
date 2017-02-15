from agents.AbstractAgent import AbstractAgent

import numpy as np
from agents.pomdp import pomdp
from TextData import TextData

import logging
logger = logging.getLogger(__name__)

class POMDPAgent(AbstractAgent):
    """
        Implementation of POMPDP agent.
        Adoption of implementation from https://github.com/mbforbes/py-pomdp
    """
    def __init__(self, domain_knowledge = None):
        super(POMDPAgent, self).__init__(domain_knowledge)

        self.observation_index = 0

        # Load 'full POMDP' using env, policy, and belief prior.
        self.model = pomdp.POMDP(
            'agents/pomdp/examples/env/voicemail.pomdp',  # env
            'agents/pomdp/examples/policy/voicemail.policy',  # policy
            np.array([[0.65], [0.35]]),  # prior
            domain_knowledge
        )

        self.terminated = False

    def process_inputs(self, inputs):
    	"""
    		Expecting a list of inputs. Each input is a list of preprocessed data.
    		This agent picks the first preprocessed data in the input.
    	"""
        if self.terminated:
            logger.info("POMDP agent already taken a terminal action. No further processing will be done.")
            return None

        inputs = [data[0].data.strip() for data in inputs]

        results = []
        best_action_str = None
        for observation in inputs:
            logger.info("Round {}".format(self.observation_index + 1))
            best_action_num, expected_reward = self.model.get_best_action()
            best_action_str = self.model.get_action_str(best_action_num)

            results.append((best_action_str, expected_reward))

            if best_action_str != 'ask':
                # We have a 'terminal' action (either 'doSave' or 'doDelete')
                self.terminated = True
                break
            else:
                # The action is 'ask': Provide our next observation.
                self.observation_index += 1
                logger.info("\t- Observation given: {}".format(observation))
                obs_num = self.model.get_obs_num(observation)
                self.model.update_belief(best_action_num, obs_num)
                # Show beliefs
                logger.info('\t- belief:         {}'.format(np.round(self.model.belief.flatten(), 3)))


        return results


    def model_postprocess(self, outputs):
        if outputs is None:
            return

        for data in outputs:
            self.queue_output(TextData("Action {}. Expected reward: {}".format(data[0], data[1])))

    def process_notification(self, content, channel):
        logger.info("Agent received notification {0} on channel {1}.".format(content, channel))