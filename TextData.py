import datetime

class TextData(object):
    def __init__(self, data, entered_time = None):
        self.entered_time = entered_time if entered_time is not None else datetime.datetime.now()
        self.data = data

    def copy_metadata_from(self, other):
    	"""
    		Copy metadata from the other object to this object. This is a shallow copy.
    	"""
    	self.entered_time = other.entered_time
