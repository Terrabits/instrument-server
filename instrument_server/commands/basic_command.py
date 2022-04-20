from .command_base   import CommandBase
from .command_parser import CommandParser


class BasicCommand(CommandBase):
    """Command Plugin base class with command, typed arg parsing"""

    command = ''
    """define command base"""

    args    = {}
    """define args, types"""

    def __init__(self, *args, **kwargs):
        CommandBase.__init__(self, *args, **kwargs)
        self.parser = CommandParser(self.command, self.args)

    def is_match(self, command_bytes):
        """returns `True` if self can execute `command_bytes`; False otherwise"""
        return self.parser.is_match(command_bytes)

    def execute(self, devices, command_bytes):
        """parses command and calls self.code"""
        # parse args
        args = self.parser.parse_args(command_bytes)

        # execute code
        return self.code(devices, args)

    def code(self, devices, args):
        """code to execute parsed command"""
