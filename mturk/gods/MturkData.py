from TextData import TextData

class MturkData(TextData):
    """
        Add conversation id to the object.
    """
    def __init__(self, conversation_id, context_id, *args, **kwargs):
        super(MturkData, self).__init__(*args, **kwargs)
        self.conversation_id = conversation_id
        self.context_id = context_id

    def copy_metadata_from(self, other):
        super(MturkData, self).copy_metadata(other)
        self.conversation_id = other.conversation_id
        self.context_id = other.context_id

    @classmethod
    def create_object_from(klass, reference, new_data):
        output = MturkData(None, None, new_data)
        output.copy_metadata_from(reference)

        return output