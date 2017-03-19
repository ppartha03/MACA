from mturk.gods import ContextFetchingInputDevice
from devices import OutputDevice

from mturk.gods import DataCollectionAgent
from mturk.gods import DatabaseListener

from preprocessing import VoidPreprocessor
from postprocessing import VoidPostprocessor

from domain_knowledge import EmptyDomainKnowledge
from conversation_listeners import LoggingListener
from conversation_listeners import Scoring

system_description = {
    'input' : {
        'class' : ContextFetchingInputDevice.ContextFetchingInputDevice,
        'kwargs' : {
            'timeout_seconds' : 0.5
        }
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
            }
        ]
    },
    'agent' : {
        'class' : DataCollectionAgent.MturkCollectionAgent
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
                'class' : LoggingListener.LoggingListener,
            },
            {
                'class' : DatabaseListener.DatabaseResponseListener,
                'args' : [ 'mturk/collected_data' ]
            }
        ]
    }
}