class ErrorQueueMixin:
    # TODO: fix error queue
    def __init__(self):
        if 'errors' not in self.state:
            self.state['errors'] = list()

    @property
    def error_queue(self):
        return self.state['errors']
