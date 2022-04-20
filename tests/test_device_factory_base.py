from   abc import ABCMeta
from   instrument_server.devices import DeviceFactoryBase
import unittest


class TestDeviceFactoryBase(unittest.TestCase):
    def test_is_ABCMeta(self):
        self.assertTrue(isinstance(DeviceFactoryBase, ABCMeta))

    def test_instantiation_raises_type_error(self):
        with self.assertRaises(TypeError):
            # this should fail
            factory = DeviceFactoryBase()

    def test_unimplemented_open_raises_type_error(self):
        class NoOpenFactory(DeviceFactoryBase):
            type = 'test'

        # is abstract class?
        self.assertTrue(isinstance(NoOpenFactory, ABCMeta))

        with self.assertRaises(TypeError):
            # this should fail
            factory = NoOpenFactory()

    def test_unimplemented_type_raises_type_error(self):
        class NoTypeFactory(DeviceFactoryBase):
            def open(self):
                pass

        # is abstract class?
        self.assertTrue(isinstance(NoTypeFactory, ABCMeta))

        with self.assertRaises(TypeError):
            # this should fail
            factory = NoTypeFactory()

    def test_complete_definition_instantiates(self):
        class FullyDefinedFactory(DeviceFactoryBase):
            type = 'device'

            def open(self):
                pass

        # is abstract class?
        self.assertTrue(isinstance(FullyDefinedFactory, ABCMeta))

        # this should work
        factory = FullyDefinedFactory()
