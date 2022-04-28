from instrument_server.commands import BasicCommand


class Command(BasicCommand):
    command = 'command'
    args    = {}

    def code(self, devices, args):
        pass


# export
IS_COMMAND_PLUGIN = True
plugin            = Command
