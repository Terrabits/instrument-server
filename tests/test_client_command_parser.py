from   ddt import ddt, data
from   instrument_server.client.command_parser import CommandParser
import unittest


@ddt
class TestClientCommandParser(unittest.TestCase):
    @data({'recv': b'',
           'commands': [],
           'data': b''},
          {'recv': b'one command\n',
           'commands': [b'one command'],
           'data': b''},
          {'recv': b'\n\none command\n',
           'commands': [b'one command'],
           'data': b''},
          {'recv': b'\n\nincomplete command',
           'commands': [],
           'data': b'incomplete command'},
          {'recv': b'command1\ncommand2\n',
           'commands': [b'command1', b'command2'],
           'data': b''})
    def test_client_command_parser(self, data):
        recv     = data['recv']
        commands = data['commands']
        data     = data['data']


        # init parser
        parser = CommandParser(initial_data=recv)

        # parse commands
        _commands = []
        while next := parser.next():
            _commands.append(next)

        # commands as expected?
        self.assertEqual(len(_commands), len(commands))
        self.assertEqual(_commands, commands)

        # data remainder as expected?
        self.assertEqual(parser.data, data)
