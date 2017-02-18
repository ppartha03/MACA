from devices import InputDevice
from devices import OutputDevice

from sample_systems.pomdp import POMDPAgent

from preprocessing import VoidPreprocessor
from postprocessing import VoidPostprocessor

from sample_systems.pomdp import POMDPDomainKnowledge
from conversation_listeners import LoggingListener
from conversation_listeners import Scoring

system_description = {
    'input' : {
        'class' : InputDevice.StdinInputDevice
    },
    'output' : {
        'class' : OutputDevice.FileOutputDevice,
        'args' : ['out.gods']
    },
    'preprocessing' : [ # Happens in parallel
        {
            'class' : VoidPreprocessor.VoidPreprocessor,
        }
    ],
    'postprocessing' : {
        'output_index' : 0, # Index of the postprocessing unit whose output will be piped to output
        'modules' : [ # Happens in parallel
            {
                'class' : VoidPostprocessor.VoidPostprocessor,
            },
            {
                'class' : VoidPostprocessor.VoidPostprocessor,
            }
        ]
    },
    'agent' : {
        'class' : POMDPAgent.POMDPAgent
    },
    'domain_knowledge' : {
        'class' : POMDPDomainKnowledge.VoiceMailPomdpDomainKnowledge
    },
    'listeners' : {
        'named' : {
            'scoring' : { 'class' : Scoring.SampleScoring }
        },
        'unnamed': [
            {
                'class' : LoggingListener.LoggingListener
            }
        ]
    }
}