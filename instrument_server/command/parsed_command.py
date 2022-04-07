from .mixin import ParserMixin


class ParsedCommand(ParserMixin):
    COMMAND = ''
    ARGS    = {}

    def __init__(self, devices, state, **settings):
        ParserMixin.__init__(self, self.COMMAND, self.ARGS)
        self.devices  = devices
        self.state    = state
        self.settings = settings

    def execute(self,  received_command):
        self.code(self.args(received_command))

    def code(self, args):
        """code to execute command"""
        pass


# # export
# IS_COMMAND_PLUGIN = True
# plugin            = ParsedCommand
