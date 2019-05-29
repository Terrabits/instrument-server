from instrument_server.command import Base
import sys

class Quit(Base):
    def is_match(self, received_command):
        return received_command.strip().lower() == b'__quit__'
    def execute(self, received_command):
        sys.exit(0)
    @property
    def help_str(self):
        return '__quit__: Shutdown server'

# # Declare as device plugin
# # for auto-import
IS_COMMAND_PLUGIN = True
plugin            = Quit
