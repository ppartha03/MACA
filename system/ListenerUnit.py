from utils import object_utils
from utils import sanity_utils

import DomainKnowledgeUser
from conversation_listeners import Scoring

class ListenerUnit(DomainKnowledgeUser.DomainKnowledgeUser):

    KNOWN_NAMES = set(('scoring', 'database'))

    @classmethod
    def construct_listener_unit(klass, description):
        named_modules = {name : object_utils.create_object(listener_class) for name, listener_class in description['named'].iteritems()}
        unnamed_modules = [object_utils.create_object(listener_class) for listener_class in description['unnamed']]

        sanity_utils.assert_subset(set(named_modules.keys()), klass.KNOWN_NAMES)
        return ListenerUnit(named_modules, unnamed_modules)

    def __init__(self, named_modules, unnamed_modules):
        super(ListenerUnit, self).__init__(list(named_modules.values()) + unnamed_modules)

        self.named_modules = named_modules
        self.unnamed_modules = unnamed_modules

    def get_named_listener(self, name):
        return self.named_modules.get(name)

    def subscribe(self, system, channels):
        for module in self.unnamed_modules:
            system.accept_subscription(module, channels)

        for module in self.named_modules.values():
            system.accept_subscription(module, channels)

        # Special listeners that publishes to the system
        if 'scoring' in self.named_modules:
            module = self.named_modules['scoring']
            assert isinstance(module, Scoring.Scoring)
            module.scoring_publisher = system