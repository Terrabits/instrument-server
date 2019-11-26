class ErrorQueueMixin(object):
    def __init__(self):
        if not 'error queue' in self.state:
            self.state['__errors__'] = list()

    @property
    def error_queue(self):
        return self.state['__errors__']
