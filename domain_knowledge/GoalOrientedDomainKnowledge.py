from domain_knowledge import AbstractDomainKnowledge

class GoalOrientedDomainKnowledge(AbstractDomainKnowledge.AbstractDomainKnowledge):
    """
        This domain knowledge hosts the slots for all intents.
    """
    def __init__(self, intent_dictionary):
        """
            Internal preprocessing of the models. Output of this will be passed on to the main internal processing of the model.
            Override if need be to perform any required internal preprocessing.

            Parameters
            ----------
            inputs : a dictionary of intent name --> list of slots for that intent.
        """
        super(GoalOrientedDomainKnowledge, self).__init__()
        self.intent_dictionary = intent_dictionary

    def get_slots(self, intent_name):
        return self.intent_dictionary.get(intent_name, [])

