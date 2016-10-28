from AbstractDomainKnowledge import AbstractDomainKnowledge

class EmptyDomainKnowledge(AbstractDomainKnowledge):
	"""
		There is nothing to know in this domain.
	"""
	def __init__(self):
		super(EmptyDomainKnowledge, self).__init__()
