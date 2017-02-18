import numpy as np
from pomdp import *

# Load 'full POMDP' using env, policy, and belief prior.
pomdp = POMDP(
    'examples/env/voicemail.pomdp',  # env
    'examples/policy/voicemail.policy',  # policy
    np.array([[0.65], [0.35]])  # prior
)

# Let's try some belief updates with the full POMDP.
observations = ['hearDelete', 'hearSave', 'hearSave']
obs_idx = 0
best_action_str = None
while True:
    print 'Round', obs_idx + 1
    best_action_num, expected_reward = pomdp.get_best_action()
    best_action_str = pomdp.get_action_str(best_action_num)
    print '\t- action:         ', best_action_str
    print '\t- expected reward:', expected_reward
    if best_action_str != 'ask':
        # We have a 'terminal' action (either 'doSave' or 'doDelete')
        break
    else:
        # The action is 'ask': Provide our next observation.
        obs_str = observations[obs_idx]
        obs_idx += 1
        print '\t- obs given:      ', obs_str
        obs_num = pomdp.get_obs_num(obs_str)
        pomdp.update_belief(best_action_num, obs_num)
        # Show beliefs
        print '\t- belief:         ', np.round(pomdp.belief.flatten(), 3)

# Take the 'terminal' action, and beliefs should be reset to prior.
best_action_num, expected_reward = pomdp.get_best_action()
pomdp.update_belief(best_action_num,
    pomdp.get_obs_num('hearSave')) # Observation doesn't affect this action.
print '\t- belief:         ', np.round(pomdp.belief.flatten(), 3)