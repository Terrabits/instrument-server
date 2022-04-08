from .mixin import parser_error, ParserMixin


class ParsedCommand(ParserMixin):
    COMMAND = ''
    ARGS    = {}

    def __init__(self, devices, state, **settings):
        ParserMixin.__init__(self, self.COMMAND, self.ARGS)
        self.devices  = devices
        self.state    = state
        self.settings = settings

    def execute(self,  received_command):
        # for raise_error
        self.received_command = received_command

        # run code, return result
        args = self.args(received_command)
        return self.code(args)

    def code(self, args):
        """code to execute command"""
        pass

    def raise_error(self, message):
        """raises CommandError"""
        parser_error(self.COMMAND, message, self.received_command)


# # export
# IS_COMMAND_PLUGIN = True
# plugin            = ParsedCommand
