from devices import InputDevice
from devices import OutputDevice

from sample_systems.echo import EchoAgent

from preprocessing import VoidPreprocessor
from postprocessing import VoidPostprocessor

from domain_knowledge import EmptyDomainKnowledge
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
    'preprocessing' : {
        'modules' : [ # Happens in parallel
            {
                'class' : VoidPreprocessor.VoidPreprocessor,
            },
            {
                'class' : VoidPreprocessor.VoidPreprocessor,
            }
        ],
        'parallel' : False
    },
    'postprocessing' : {
        'output_index' : 0, # Index of the postprocessing unit whose output will be piped to output
        'parallel' : False,
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
        'class' : EchoAgent.EchoAgent
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
