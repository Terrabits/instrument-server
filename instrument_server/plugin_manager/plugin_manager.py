from .command_plugin_manager  import CommandPluginManager
from .device_factory_plugin_manager  import DeviceFactoryPluginManager
from .helpers                 import load_module
from instrument_server.errors import PluginError


class PluginManager:
    def __init__(self):
        self.commands_manager         = CommandPluginManager()
        self.device_factories_manager = DeviceFactoryPluginManager()

    def register_plugins(self, modules):
        for module in modules:
            self.register_plugin(module)

    def register_plugin(self, module):
        module = load_module(module)
        if self.commands_manager.register_plugin(module):
            # module is command plugin
            return
        if self.device_factories_manager.register_plugin(module):
            # module is device factory plugin
            return

        # module is not plugin
        message = f'module {module} is not recognized as a plugin'
        raise PluginError(message)

    @property
    def commands(self):
        return self.commands_manager.plugins

    @property
    def device_factories(self):
        return self.device_factories_manager.plugins
