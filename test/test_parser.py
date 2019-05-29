from   ddt                import ddt, data
from   instrument_server.parser import Parser
import unittest

@ddt
class TestParser(unittest.TestCase):
    @data(
        {'initial_data': b'',
        'command_list': [],
        'final_data': b''},
        {'initial_data': b'one command\n',
        'command_list': [b'one command'],
        'final_data': b''},
        {'initial_data': b'\n\none command\n',
        'command_list': [b'one command'],
        'final_data': b''},
        {'initial_data': b'\n\nincomplete command',
        'command_list': [],
        'final_data': b'incomplete command'},
        {'initial_data': b'command1\ncommand2\n',
        'command_list': [b'command1', b'command2'],
        'final_data': b''})
    def test_parser(self, data):
        initial_data = data['initial_data']
        final_data   = data['final_data'  ]
        command_list = data['command_list']

        parser = Parser(initial_data)
        this_command_list = []
        next_command = parser.next_command()
        while next_command:
            this_command_list.append(next_command)
            next_command = parser.next_command()
        self.assertEqual(this_command_list, command_list)
        self.assertEqual(parser.data, final_data)
