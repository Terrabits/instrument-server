from .base  import Base
from .mixin import ParserMixin
import sys

class Quit(ParserMixin, Base):
    def __init__(self, devices, state, **settings):
        Base       .__init__(self, devices, state, **settings)
        ParserMixin.__init__(self, command="__quit__")

    @property
    def help_str(self):
        return '__quit__: Shutdown server'

    def execute(self, received_command):
        sys.exit(0)


# # Declare as device plugin
# # for auto-import
IS_COMMAND_PLUGIN = True
plugin            = Quit
