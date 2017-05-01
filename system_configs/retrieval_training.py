from devices import InputDevice
from devices import OutputDevice

from sample_systems.retrieval_model import RetrievalModelAgent
from sample_systems.retrieval_model import RetrievalModelTrainingInputDevice
from sample_systems.retrieval_model import RetrievalModelPreprocessor
from sample_systems.retrieval_model import RetrievalDomainKnowledge

from preprocessing import VoidPreprocessor
from postprocessing import VoidPostprocessor

from domain_knowledge import EmptyDomainKnowledge
from conversation_listeners import LoggingListener
from conversation_listeners import Scoring

from system import system_modes

system_description = {
    'input' : {
        'class' : RetrievalModelTrainingInputDevice.RetrievalModelTrainingInputDevice,
        'kwargs' : {
            'n_epochs' : 1,
            'shuffle_batch' : False
        }
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
        'class' : RetrievalModelAgent.RetrievalModelAgent,
        'args' : [
            'sample_systems/retrieval_model/twitter_dataset/W_twitter_bpe.pkl'
        ],
        'kwargs' : {
            'model_fname' : 'model.pkl',
            'mode' : system_modes.TRAINING,
            'model_params' : {
                'encoder' : 'lstm',
                'batch_size' : 512,
                'hidden_size' : 200,
                'optimizer' : 'adam',
                'lr' : 0.001,
                'fine_tune_W' : True,
                'fine_tune_M' : True,
                # 'input_dir' : '../../twitter_dataset',
                # 'W_fname' : 'W_twitter_bpe.pkl'
            }
        }
    },
    'domain_knowledge' : {
        'class' : EmptyDomainKnowledge.EmptyDomainKnowledge
    },
    'dataset' : {
        'class' : RetrievalDomainKnowledge.RetrievalTwitterDataset,
        'args' : ['./sample_systems/retrieval_model/twitter_dataset', 'dataset_twitter_bpe.pkl']
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