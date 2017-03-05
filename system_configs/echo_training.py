from devices import InputDevice
from devices import OutputDevice

from sample_systems.echo import EchoAgent
from sample_systems.echo import EchoTrainingInput

from preprocessing import VoidPreprocessor
from postprocessing import VoidPostprocessor

from domain_knowledge import EmptyDomainKnowledge
from conversation_listeners import LoggingListener
from conversation_listeners import Scoring

from system import system_modes

system_description = {
    'input' : {
        'class' : EchoTrainingInput.EchoTrainingInput,
        'kwargs' : {
            'max_epochs' : 10
        }
    },
    'output' : {
        'class' : OutputDevice.VoidOutputDevice,
    },
    'preprocessing' : [ # Happens in parallel
        {
            'class' : VoidPreprocessor.VoidPreprocessor,
        },
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
        'class' : EchoAgent.EchoAgent,
        'kwargs' : {
            'mode' : system_modes.TRAINING
        }
    },
    'domain_knowledge' : {
        'class' : EmptyDomainKnowledge.EmptyDomainKnowledge
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