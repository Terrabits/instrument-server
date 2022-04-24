from .basic_command import BasicCommand
import sys


class QuitCommand(BasicCommand):
    """`quit`

    Shuts down the server
    """

    # definition
    command = 'quit'
    args    = {}

    # implementation
    def code(self, devices, args):
        sys.exit(0)


# export
IS_COMMAND_PLUGIN = True
plugin            = QuitCommand
