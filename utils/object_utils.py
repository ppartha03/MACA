

def create_object(description):
	"""
		Create an object from the class constructor with args and kwargs.
		the description is a dictionary with the following keys:
			1) 'class': the class of the object
			2) args : optional args for class constructor
			3) kwargs : optional kwargs for class constructor
	"""
	klass = description['class']
	args = description.get('args', [])
	kwargs = description.get('kwargs', {})

	return klass(*args, **kwargs)