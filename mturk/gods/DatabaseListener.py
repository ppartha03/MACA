import abc
import os
import logging
from datetime import datetime

from system import system_channels
from conversation_listeners.AbstractConversationListener import AbstractConversationListener

logger = logging.getLogger(__name__)

class _BaseMturkListener(AbstractConversationListener):
    """
        Base listener for mturk operations.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, db_dir):
        super(_BaseMturkListener, self).__init__()
        self.db_dir = db_dir

    def _get_conversation_file(self, conversation_id):
        return os.path.join(self.db_dir, conversation_id)

    def _write_data(self, file_object, prefix, data):
        file_object.write('[{}] --> '.format(prefix))
        file_object.write(data)
        file_object.write('\n')

class DatabaseResponseListener(_BaseMturkListener):
    """
        Record user's responses.
    """
    def __init__(self, db_dir):
        super(DatabaseResponseListener, self).__init__(db_dir)

    def process_notification(self, content, channel):
        if channel == system_channels.INPUT:
            for utterance in content:
                with open(self._get_conversation_file(utterance.conversation_id), 'a') as f:
                    self._write_data(f, 'Input', utterance.data)

        elif channel == system_channels.OUTPUT:
            utterance = content[0] # Only write one processed output

            with open(self._get_conversation_file(utterance.conversation_id), 'a') as f:
                self._write_data(f, 'Output', utterance.data)

def pp(didi):
    print "====================================================="
    for k, v in didi.iteritems():
        count = 0
        if hasattr(v, 'data'):
            count = 1
            if hasattr(v.data, 'data'):
                count = 2
        print "{} --> {}".format(k, count)
    print "====================================================="

class DatabaseScoringListener(_BaseMturkListener):
    """
        Record user's context as well as score.
    """
    def __init__(self, db_dir):
        super(DatabaseScoringListener, self).__init__(db_dir)
        self.context_awaiting = {}
        self.response_awaiting = {}

    def process_notification(self, content, channel):
        if channel == system_channels.INPUT:
            for utterance in content:
                utterance = content[0]
                self.context_awaiting[utterance.context_id] = utterance
        elif channel == system_channels.OUTPUT:
            utterance = content[0] # Only write one processed output
            self.response_awaiting[utterance.context_id] = utterance
        elif channel == system_channels.SCORING:
            context_id = content.context_id
            if context_id not in self.response_awaiting:
                return

            if context_id not in self.context_awaiting:
                return

            context = self.context_awaiting.pop(context_id)
            response = self.response_awaiting.pop(context_id)

            with open(self._get_conversation_file(content.conversation_id), 'a') as f:
                self._write_data(f, 'Input', context.data)
                self._write_data(f, 'Output', '[{}] {}'.format(content.data, response.data.data))