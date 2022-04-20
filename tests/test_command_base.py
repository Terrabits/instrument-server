from   abc import ABCMeta
from   instrument_server.commands import CommandBase
import unittest


class TestCommandBase(unittest.TestCase):
    def test_is_ABCMeta(self):
        self.assertTrue(isinstance(CommandBase, ABCMeta))

    def test_instantiation_raises_type_error(self):
        with self.assertRaises(TypeError):
            # this should fail
            factory = CommandBase()

    def test_unimplemented_is_match_raises_type_error(self):
        class NoIsMatchCommand(CommandBase):
            def execute(self, devices, state, command_bytes):
                pass

        # is abstract class?
        self.assertTrue(isinstance(NoIsMatchCommand, ABCMeta))

        with self.assertRaises(TypeError):
            # this should fail
            command = NoIsMatchCommand()

    def test_unimplemented_execute_raises_type_error(self):
        class NoExecuteCommand(CommandBase):
            def is_match(self, command_bytes):
                pass

        # is abstract class?
        self.assertTrue(isinstance(NoExecuteCommand, ABCMeta))

        with self.assertRaises(TypeError):
            # this should fail
            command = NoExecuteCommand()

    def test_complete_definition_instantiates(self):
        class FullyDefinedCommand(CommandBase):
            def is_match(self, command_bytes):
                pass

            def execute(self, devices, state, command_bytes):
                pass

        # is abstract class?
        self.assertTrue(isinstance(FullyDefinedCommand, ABCMeta))

        # this should work
        command = FullyDefinedCommand()
