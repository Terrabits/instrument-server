from .base  import Base
from .mixin import ErrorQueueMixin, ParserMixin

class Error(ErrorQueueMixin, ParserMixin, Base):
    def __init__(self, devices, state, **settings):
        Base           .__init__(self, devices, state, **settings)
        ParserMixin    .__init__(self, command='errors?')
        ErrorQueueMixin.__init__(self)
        self.state['__errors__'] = []

    @property
    def help_str(self):
        return 'Returns errors currently in queue:\n `errors?`'

    def execute(self, received_command):
        args = self.args(received_command)
        prev_errors = self.error_queue
        self.error_queue.clear()
        return prev_errors

# # Declare as device plugin
# # for auto-import
IS_COMMAND_PLUGIN = True
plugin            = Error
