import abc

class DomainKnowledgeUser(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, modules):
        super(DomainKnowledgeUser, self).__init__()
        self.modules = modules

    def set_domain_knowledge(self, domain_knowledge):
        for module in self.modules:
            self.domain_knowledge = domain_knowledge