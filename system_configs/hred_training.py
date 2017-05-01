from devices import InputDevice
from devices import OutputDevice

from system import system_modes

from sample_systems.hred.gods_agent import hred_agent

from sample_systems.hred.gods_agent import HREDTrainingInputDevice
from preprocessing import VoidPreprocessor
from postprocessing import VoidPostprocessor

from domain_knowledge import EmptyDomainKnowledge
from conversation_listeners import LoggingListener
from conversation_listeners import Scoring

system_description = {
    'input' : {
        'class' : HREDTrainingInputDevice.HREDTrainingInputDevice
        # 'class' : InputDevice.StdinInputDevice
    },
    'output' : {
        'class' : OutputDevice.FileOutputDevice,
        'args' : ['out.gods']
    },
    'preprocessing' : {
        'modules': [
            {
                'class' : VoidPreprocessor.VoidPreprocessor,
            }
        ]
    },
    'postprocessing' : {
        'output_index' : 0, # Index of the postprocessing unit whose output will be piped to output
        'modules' : [
            {
                'class' : VoidPostprocessor.VoidPostprocessor,
            }
        ]
    },
    'agent' : {
        'class' : hred_agent.HREDAgent,
        'kwargs' : {
            'mode' : system_modes.TRAINING
        }
    },
    'domain_knowledge' : {
        'class' : EmptyDomainKnowledge.EmptyDomainKnowledge
    },
    'listeners' : {
        'named' : {
            # 'scoring' : { 'class' : Scoring.SampleScoring }
        },
        'unnamed': [
            {
                'class' : LoggingListener.LoggingListener
            }
        ]
    }
}