from .helpers                 import is_plugin
from instrument_server.errors import PluginError
from importlib                import import_module


class DeviceFactoryPluginManager:
    def __init__(self):
        self.plugins = []

    def register_plugin(self, module):
        # is plugin?
        if not is_plugin(module):
            return False

        plugin = module.plugin

        # already registered?
        if plugin in self.plugins:
            message = f"device plugin {plugin} is already registered"
            raise PluginError(message)

        # register
        self.plugins.append(plugin)
        return True
