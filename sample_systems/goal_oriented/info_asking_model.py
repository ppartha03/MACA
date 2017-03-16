from system import system_modes
from agents import goal_oriented_model as model

class NameAskingPolicy(model.IntentPolicy):
    """
        Simple tokenizer to parse the name that the user provides.
    """
    def __init__(self, slots):
        super(NameAskingPolicy, self).__init__(slots)

    def get_info(self, sentence):
        tokens = sentence.strip().split(', ')
        while len(tokens) < 2:
            tokens.append(None)

        self.slots['first_name'].fill_value(tokens[0])
        self.slots['last_name'].fill_value(tokens[1])

        return self.get_unfinished_slots()

    def ask_info(self, unfilled_slots):
        return "Could you please provide your name in form of [first name], [last name]?"

    def get_confirmation(self, sentence):
        return "yes" in sentence.lower()

    def action_with_information(self):
        """
            Concrete action that the system will do once goal is achieved (all information collected).
        """
        print "Collected name. My job here is done."

class AddressAskingPolicy(model.IntentPolicy):
    """
        Simple tokenizer to parse the address that the user provides.
    """
    def __init__(self, slots):
        super(AddressAskingPolicy, self).__init__(slots)

    def get_info(self, sentence):
        tokens = sentence.strip().split(', ')
        while len(tokens) < 4:
            tokens.append(None)

        self.slots['street'].fill_value(tokens[0], 'apt')
        self.slots['street'].fill_value(tokens[1], 'street_name')

        self.slots['city'].fill_value(tokens[2])
        self.slots['country'].fill_value(tokens[3])

        if len(tokens) == 5:
            self.slots['zip_code'].fill_value(tokens[4])

        return self.get_unfinished_slots()

    def ask_info(self, unfilled_slots):
        return "Could you please provide your address in form of [apt], [street], [city], [country], [zip code if in US]?"

    def get_confirmation(self, sentence):
        return "yes" in sentence.lower()

    def action_with_information(self):
        return "Collected address. My job here is done."


class PersonalInformationAskingModel(model.GoalOrientedModel):
    """
        Asking for name or address.
    """
    def __init__(self, intents = [], domain_knowledge = None, mode = system_modes.EXECUTION):
        super(PersonalInformationAskingModel, self).__init__(intents, domain_knowledge, mode)

    def get_intent(self, sentence):
        if 'address' in sentence:
            self.current_intent = self.intents[0]
            return True

        if 'name' in sentence:
            self.current_intent = self.intents[1]
            return True

        return False

    def ask_intent(self):
        return "Hi. Please choose between asking name and asking address."

    def model_preprocess(self, inputs):
        return [data[0].data for data in inputs]