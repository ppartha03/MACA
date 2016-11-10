import abc

class Publisher(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(Publisher, self).__init__()
        self.subscription_list = []

    def accept_subscription(self, subscriber):
        self.subscription_list.append(subscriber)


    def publish(self, content, tag = None):
        for subscriber in self.subscription_list:
            subscriber.notify(content, tag)


class Subscriber(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, interested_tags = None):
        super(Subscriber, self).__init__()
        self.interested_tags = interested_tags # If none then listen to everything

    def notify(self, content, tag):
        if self.interested_tags is None or tag in self.interested_tags:
            self.process_notification(content, tag)

    @abc.abstractmethod
    def process_notification(self, content, tag):
        pass