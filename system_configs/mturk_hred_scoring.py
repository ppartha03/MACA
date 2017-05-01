from mturk.gods import ContextReceivingInputDevice
from mturk.gods import NotifiedResponseOutputDevice

from mturk.gods import DatabaseListener
from mturk.gods import mturk_scoring_adapters

from sample_systems.hred.gods_agent import hred_agent

from sample_systems.hred import hred_preprocessing
from postprocessing import VoidPostprocessor

from domain_knowledge import EmptyDomainKnowledge
from conversation_listeners import LoggingListener
from conversation_listeners import Scoring

system_description = {
    'input' : {
        'class' : ContextReceivingInputDevice.ContextReceivingInputDevice,
        'kwargs' : {
            'timeout_seconds' : 0.5
        }
    },
    'output' : {
        'class' : NotifiedResponseOutputDevice.NotifiedResponseOutputDevice,
        'args' : ['out.gods']
    },
    'preprocessing' : {
        'modules': [
            {
                'class' : mturk_scoring_adapters.MturkScoringPreprocessingAdapter,
                'args' : [ hred_preprocessing.HredPreprocessor ]
            }
        ]
    },
    'postprocessing' : {
        'output_index' : 0, # Index of the postprocessing unit whose output will be piped to output
        'modules' : [
            {
                'class' : mturk_scoring_adapters.MturkScoringPostProcessing,
                'args' : [ VoidPostprocessor.VoidPostprocessor ]
            }
        ]
    },
    'agent' : {
        'class' : mturk_scoring_adapters.MturkScoringAgentAdapter,
        'args' : [ hred_agent.HREDAgent ],
        'kwargs' : {
            'ignore_unknown_words' : True,
            'normalize' : False,
            'dictionary_path' : '/home/ml/rlowe1/UbuntuData/Dataset.dict.pkl',
            'model_prefix' : '/home/2016/pparth2/Desktop/gods/Goal-Oriented_Dialogue_Systems/Pre-Trained_HRED_Model/drive-download-20161021T162213Z/1453999317.44_UbuntuModel_HRED/1453999317.44_UbuntuModel_HRED'
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
            },
            {
                'class' : DatabaseListener.DatabaseScoringListener,
                'args' : [ 'mturk/collected_data' ]
            }
        ]
    }
}