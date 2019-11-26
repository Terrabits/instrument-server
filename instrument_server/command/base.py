# to declare command for auto-import.
# See below class definition.

class Base(object):
    def __init__(self, devices, state, **settings):
        self.devices  = devices
        self.state    = state
        self.settings = settings
    def is_match(self, received_command):
        return False
    def execute(self,  received_command):
        pass
    @property
    def help_str(self):
        return ''

# # Declare as device plugin
# # for auto-import
# IS_COMMAND_PLUGIN = True
# plugin            = Base
