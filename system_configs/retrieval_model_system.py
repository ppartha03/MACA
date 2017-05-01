from devices import InputDevice
from devices import OutputDevice

from sample_systems.retrieval_model import RetrievalModelAgent
from sample_systems.retrieval_model import RetrievalModelInputDevice
from sample_systems.retrieval_model import RetrievalModelPreprocessor

from postprocessing import VoidPostprocessor

from domain_knowledge import EmptyDomainKnowledge
from conversation_listeners import LoggingListener
from conversation_listeners import Scoring

system_description = {
    'input' : {
        'class' : RetrievalModelInputDevice.RetrievalModelInputDevice,
        'args' : ['sample_systems/retrieval_model/sample_execution_input_data.txt']
    },
    'output' : {
        'class' : OutputDevice.FileOutputDevice,
        'args' : ['out.gods']
    },
    'preprocessing' : {
        'modules': [ # Happens in parallel
            {
                'class' : RetrievalModelPreprocessor.RetrievalModelPreprocessor,
                'args' : ['sample_systems/retrieval_model/BPE/Twitter_Codes_5000.txt']
            }
        ]
    },
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
        'class' : RetrievalModelAgent.RetrievalModelAgent,
        'args' : [
            'sample_systems/retrieval_model/twitter_dataset/W_twitter_bpe.pkl'
        ],
        'kwargs' : {
            'model_params' : {
                'encoder' : 'lstm',
                'batch_size' : 512,
                'hidden_size' : 100,
                'optimizer' : 'adam',
                'lr' : 0.001,
                'fine_tune_W' : True,
                'fine_tune_M' : True,
                'input_dir' : '../../twitter_dataset',
                'W_fname' : 'W_twitter_bpe.pkl'
            }
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