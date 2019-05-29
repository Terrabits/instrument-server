from   ddt                     import ddt, data
from   instrument_server.command     import Translation
from   instrument_server.test.device import Test
import unittest

@ddt
class TestTranslation(unittest.TestCase):
    @data(
        {'definition':         'cmd_no_args',
         'command':            'cmd_no_args',
         'is_query':           False,
         'arg_names':          []},
        {'definition':         'cmd_1_arg arg1',
         'command':            'cmd_1_arg',
         'is_query':           False,
         'arg_names':          ['arg1']},
        {'definition':         'cmd_3_args arg1 arg2 arg3',
         'command':            'cmd_3_args',
         'is_query':           False,
         'arg_names':          ['arg1', 'arg2', 'arg3']},
        {'definition':         'cmd_query_no_args?',
         'command':            'cmd_query_no_args?',
         'is_query':           True,
         'arg_names':          []},
        {'definition':         'cmd_query_1_arg? arg1',
         'command':            'cmd_query_1_arg?',
         'is_query':           True,
         'arg_names':          ['arg1']}
    )
    def test_definition(self, data):
        definition = data['definition']
        command    = data['command']
        is_query   = data['is_query']
        arg_names  = data['arg_names']

        outgoing_commands = []
        devices           = {}
        t = Translation(definition, outgoing_commands, devices)
        self.assertEqual(t.command,   command)
        self.assertEqual(t.is_query,  is_query)
        self.assertEqual(t.arg_names, arg_names)

    @data(
        {'definition':         'my_command',
         'received_command':  b'MY_COMMAND',
         'is_match':           True},
        {'definition':         'my_command',
         'received_command':  b'not_my_command',
         'is_match':           False})
    def test_is_match(self, data):
        definition       = data['definition']
        received_command = data['received_command']
        is_match         = data['is_match']

        outgoing_commands = []
        devices           = {}
        t = Translation(definition, outgoing_commands, devices)
        self.assertEqual(t.is_match(received_command), is_match)

    @data(
    {'definition':         'cmd_no_args',
     'outgoing_commands':  [{'test': 'SCPI:NO:ARG'}],
     'received_command':  b'cmd_no_args',
     'writes':             [b'SCPI:NO:ARG'],
     'return_value':       None},
    {'definition':         'cmd_1_arg arg1',
     'outgoing_commands':  [{'test': 'SCPI:ONE:ARG {arg1}'}],
     'received_command':  b'cmd_1_arg 10',
     'writes':             [b'SCPI:ONE:ARG 10'],
     'return_value':       None})
    def test_execute(self, data):
        definition        = data['definition']
        received_command  = data['received_command' ]
        outgoing_commands = data['outgoing_commands']
        writes            = data['writes']
        return_value      = data['return_value']

        test_device = Test(reads=[return_value])
        devices     = {'test': test_device}

        t = Translation(definition, outgoing_commands, devices)
        self.assertTrue (t.is_match(received_command))
        self.assertEqual(t.execute(received_command), return_value)
        self.assertEqual(test_device.writes,          writes)
