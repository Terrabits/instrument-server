from   ddt                              import ddt, data
from   instrument_server.commands       import QuitCommand
from   instrument_server.devices        import SocketFactory
from   instrument_server.errors         import PluginError
from   instrument_server.plugin_manager import PluginManager
import unittest


@ddt
class TestPluginManager(unittest.TestCase):
    def test_instantiation(self):
        plugin_manager = PluginManager()
        self.assertEqual(plugin_manager.commands,         [])
        self.assertEqual(plugin_manager.device_factories, [])

    def test_register_command_plugin(self):
        plugin_manager = PluginManager()
        plugin_manager.register_plugin('tests.mock.command_plugin')

    def test_register_device_factory_plugin(self):
        plugin_manager = PluginManager()
        plugin_manager.register_plugin('tests.mock.device_factory_plugin')

    def test_raises_module_not_found_error(self):
        plugin_manager = PluginManager()
        with self.assertRaises(ModuleNotFoundError):
            plugin_manager.register_plugin('module.is.missing')

    def test_raises_module_not_plugin_error(self):
        plugin_manager = PluginManager()
        with self.assertRaises(PluginError):
            plugin_manager.register_plugin('builtins')

    def test_raises_plugin_already_registered_error(self):
        plugin_manager = PluginManager()
        plugin_manager.register_plugin('tests.mock.command_plugin')
        with self.assertRaises(PluginError):
            plugin_manager.register_plugin('tests.mock.command_plugin')
