from devices import InputDevice
from devices import OutputDevice
from agents.sample_agents.EchoAgent import EchoAgent

from preprocessing import VoidPreprocessor
from postprocessing import VoidPostprocessor

system_description = {
    'input' : {
        'class' : InputDevice.StdinInputDevice
    },
    'output' : {
        'class' : OutputDevice.FileOutputDevice,
        'args' : ['out.gods']
    },
    'preprocessing' : {
        'class' : VoidPreprocessor.VoidPreprocessor,
    },
    'postprocessing' : {
        'class' : VoidPostprocessor.VoidPostprocessor,
    },
    'agent' : {
        'class' : EchoAgent
    }
}