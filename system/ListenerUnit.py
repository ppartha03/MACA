from utils import object_utils
import DomainKnowledgeUser

class ListenerUnit(DomainKnowledgeUser.DomainKnowledgeUser):

    @classmethod
    def construct_listener_unit(klass, description):
        modules = [object_utils.create_object(listener_class) for listener_class in description]
        return ListenerUnit(modules)

    def __init__(self, modules):
        super(ListenerUnit, self).__init__(modules)

    def listen_to_inputs(self, inputs):
        for data in inputs:
            for module in self.modules:
                module.listen_to_input(data)

    def listen_to_output(self, postprocess_channels):
        for module in self.modules:
            module.listen_to_output(postprocess_channels)