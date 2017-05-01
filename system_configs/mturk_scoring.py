from mturk.gods import ContextReceivingInputDevice
from mturk.gods import NotifiedResponseOutputDevice

from mturk.gods import DatabaseListener
from mturk.gods import mturk_scoring_adapters

from sample_systems.echo import EchoAgent

from preprocessing import VoidPreprocessor
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
                'args' : [ VoidPreprocessor.VoidPreprocessor ]
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
        'args' : [ EchoAgent.EchoAgent ]
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