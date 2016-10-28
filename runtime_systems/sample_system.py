from devices import InputDevice
from devices import OutputDevice
from agents.sample_agents import EchoAgent

from preprocessing import VoidPreprocessor
from postprocessing import VoidPostprocessor

from domain_knowledge import EmptyDomainKnowledge

system_description = {
    'input' : {
        'class' : InputDevice.StdinInputDevice
    },
    'output' : {
        'class' : OutputDevice.FileOutputDevice,
        'args' : ['out.gods']
    },
    'preprocessing' : [
        {
            'class' : VoidPreprocessor.VoidPreprocessor,
        },
        {
            'class' : VoidPreprocessor.VoidPreprocessor,
        }
    ],
    'postprocessing' : [
        {
            'class' : VoidPostprocessor.VoidPostprocessor,
        },
        {
            'class' : VoidPostprocessor.VoidPostprocessor,
        }
    ],
    'agent' : {
        'class' : EchoAgent.EchoAgent
    },
    'domain_knowledge' : {
        'class' : EmptyDomainKnowledge.EmptyDomainKnowledge
    }
}