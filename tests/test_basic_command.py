from   ddt import ddt, data
from   instrument_server.commands import BasicCommand
from   instrument_server.errors   import CommandError
import unittest


# constants
NO_DEVICES  = {}


@ddt
class TestBasicCommand(unittest.TestCase):
    @data({'definition':    {'command': 'reset', 'args': {}},
           'recv':          b'random',
           'is_match':      False,
           'exception':     None,
           'expected_args': {}},
          {'definition':    {'command': 'reset', 'args': {}},
           'recv':          b'reset',
           'is_match':      True,
           'exception':     None,
           'expected_args': {}},
          {'definition':    {'command': 'reset', 'args': {}},
           'recv':          b'reset with too many args',
           'is_match':      True,
           'exception':     CommandError,
           'expected_args': {}})
    def test_basic_command(self, data):
        # get test data
        definition    = data['definition']
        recv          = data['recv']
        is_match      = data['is_match']
        exception     = data['exception']
        expected_args = data['expected_args']

        # nonlocals for use in TestCommand
        code_was_called = False
        test_obj        = self

        # define command

        class TestCommand(BasicCommand):
            command = definition['command']
            args    = definition['args']

            def code(self, devices, args):
                nonlocal code_was_called
                nonlocal test_obj
                code_was_called = True
                test_obj.assertEqual(devices, NO_DEVICES)
                test_obj.assertEqual(args,    expected_args)

        # create new
        command = TestCommand()

        # is match?
        self.assertEqual(command.is_match(recv), is_match)
        if not is_match:
            # end of test
            return

        # is match

        if exception:
            # should raise exception
            with self.assertRaises(exception):
                command.execute(NO_DEVICES, recv)
            return

        # execute
        command.execute(NO_DEVICES, recv)

        # code was called?
        self.assertTrue(code_was_called)
