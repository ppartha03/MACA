from devices import InputDevice
from devices import OutputDevice

from sample_systems.hred.gods_agent import hred_agent

from sample_systems.hred import hred_preprocessing
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
        'modules': [
            {
                'class' : hred_preprocessing.HredPreprocessor,
            }
        ]
    },
    'postprocessing' : {
        'output_index' : 0, # Index of the postprocessing unit whose output will be piped to output
        'modules' : [
            {
                'class' : VoidPostprocessor.VoidPostprocessor,
            },
            {
                'class' : VoidPostprocessor.VoidPostprocessor,
            }
        ]
    },
    'agent' : {
        'class' : hred_agent.HREDAgent,
        'kwargs' : {
            'ignore_unknown_words' : True,
            'normalize' : False,

            # 'prototype' : 'prototype_ubuntu_HRED',
            # 'train_dialogues' : "/home/ml/rlowe1/UbuntuData/Training.dialogues.pkl",
            # 'test_dialogues' : "/home/ml/rlowe1/UbuntuData/Test.dialogues.pkl",
            # 'valid_dialogues' : "/home/ml/rlowe1/UbuntuData/Validation.dialogues.pkl",
            # 'dictionary_path' : '/home/ml/rlowe1/UbuntuData/Dataset.dict.pkl',
            'prototype' : 'prototype_twitter_HRED',
            'train_dialogues' : '/home/ml/rlowe1/TwitterData/Training.dialogues.pkl',
            'test_dialogues' : '/home/ml/rlowe1/TwitterData/Test.dialogues.pkl',
            'valid_dialogues' : '/home/ml/rlowe1/TwitterData/Validation.dialogues.pkl',
            'dictionary_path' : '/home/ml/rlowe1/TwitterData/Dataset.dict.pkl',

            # 'model_prefix' : '/home/2016/pparth2/Desktop/gods/Goal-Oriented_Dialogue_Systems/Pre-Trained_HRED_Model/drive-download-20161021T162213Z/1453999317.44_UbuntuModel_HRED/1453999317.44_UbuntuModel_HRED'
            # 'model_prefix' : '/home/ml/rlowe1/TwitterData/hred_twitter_models/1470516214.08_TwitterModel__405001'
            'model_prefix' : '/home/2016/pparth2/Desktop/gods/Goal-Oriented_Dialogue_Systems/Pre-Trained_Twitter_Model/1450650334.74_TwitterModel'
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