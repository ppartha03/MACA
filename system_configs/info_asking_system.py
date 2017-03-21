from devices import InputDevice
from devices import OutputDevice

from agents.goal_oriented_model import Slot
from sample_systems.goal_oriented import info_asking_model

from preprocessing import VoidPreprocessor
from postprocessing import VoidPostprocessor

from domain_knowledge import GoalOrientedDomainKnowledge
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
            }
        ]
    },
    'agent' : {
        'class' : info_asking_model.PersonalInformationAskingModel,
        'kwargs' : {
            'intents' : [
                info_asking_model.AddressAskingPolicy('address'),
                info_asking_model.NameAskingPolicy('name')
            ]
        }
    },
    'domain_knowledge' : {
        'class' : GoalOrientedDomainKnowledge.GoalOrientedDomainKnowledge,
        'args' : [
            {
                'address' : [
                    Slot('street', ['apt', 'street_name']),
                    Slot('city'),
                    Slot('country'),
                    Slot('zip_code', enabling_condition = lambda slots: slots['country'].get_value() == "US")
                ],
                'name' : [
                    Slot('first_name'),
                    Slot('last_name')
                ],
                'restaurant_booking' : [
                    Slot('cuisine'),
                    Slot('location'),
                    Slot('price')
                ],
                'flight_booking' : [
                    Slot('origin'),
                    Slot('destination'),
                    Slot('passenger_count'),
                    Slot('price_range'),
                    Slot('depart_date'),
                    Slot('is_round_trip'),
                    Slot('return_date', enabling_condition = lambda slots: slots['is_round_trip'].get_value() == True)
                ]
            }
        ]
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