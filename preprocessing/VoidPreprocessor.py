from preprocessing.AbstractPreprocessor import AbstractPreprocessor

class VoidPreprocessor(AbstractPreprocessor):
	"""
		Does nothing to the input.
	"""
	def __init__(self):
		super(VoidPreprocessor, self).__init__()

	def preprocess(self, data):
		return data