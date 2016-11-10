

def _base_assert(fact):
	assert fact

def assert_in(element, iterable):
	_base_assert(element in iterable)

def assert_subset(set1, set2):
	_base_assert(set1.issubset(set2))

def assert_true(condition):
	_base_assert(condition is True)

def assert_false(condition):
	_base_assert(condition is False)