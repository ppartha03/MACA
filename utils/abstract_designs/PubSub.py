import abc

class Publisher(object):

    def __init__(self):
        super(Publisher, self).__init__()
        self.subscription_list = {}

    def _add_subscriber(self, subscriber, channel):
        if channel not in self.subscription_list:
            self.subscription_list[channel] = set()

        self.subscription_list[channel].add(subscriber)

    def accept_subscription(self, subscriber, channels = ()):
        """
            Add the subscriber to the appropriate listening channels.
        """
        for channel in channels:
            self._add_subscriber(subscriber, channel)

    def publish(self, content, channel = None):
        """
            Publish a content to a channel.
        """
        for subscriber in self.subscription_list.get(channel, []):
            subscriber.notify(content, channel)


class Subscriber(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(Subscriber, self).__init__()

    def notify(self, content, channel):
        self.process_notification(content, channel)

    @abc.abstractmethod
    def process_notification(self, content, channel):
        pass