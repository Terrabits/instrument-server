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

    def test_register_socket_factory(self):
        plugin_manager = PluginManager()
        plugin_manager.register_plugin('instrument_server.devices.socket_factory')
        self.assertEqual(plugin_manager.device_factories, [SocketFactory])

    def test_register_quit_command(self):
        plugin_manager = PluginManager()
        plugin_manager.register_plugin('instrument_server.commands.quit_command')
        self.assertEqual(plugin_manager.commands, [QuitCommand])

    def test_raises_module_not_found_error(self):
        plugin_manager = PluginManager()
        with self.assertRaises(ModuleNotFoundError):
            plugin_manager.register_plugin('module.is.missing')

    def test_module_not_plugin_raises_plugin_error(self):
        plugin_manager = PluginManager()
        with self.assertRaises(PluginError):
            plugin_manager.register_plugin('builtins')

    def test_reregistering_plugin_raises_plugin_error(self):
        plugin_manager = PluginManager()

        # first register should succeed
        plugin_manager.register_plugin('instrument_server.devices.socket_factory')

        with self.assertRaises(PluginError):
            # this should fail
            plugin_manager.register_plugin('instrument_server.devices.socket_factory')
