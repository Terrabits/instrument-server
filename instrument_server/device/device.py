from importlib import import_module
from pathlib   import Path

class DeviceError(Exception):
    pass

def register_plugin(module):
    try:
        if type(module) == str:
            module = import_module(module)
        if not is_plugin(module):
            return False
        name, plugin = get_plugin_pair(module)
        name = name.strip().lower()
        if name in plugins:
            # alert on potential overwrite
            assert plugins[name] == plugin
        plugins[name] = plugin
        return True
    except:
        return False
def remove_plugin(name):
    if name in plugins:
        del plugins[name]

def is_plugin(module):
    try:
        module.IS_DEVICE_PLUGIN
        return True
    except:
        return False
def get_plugin_pair(module):
    assert is_plugin(module)
    return module.plugin_name, module.plugin

# plugins
plugins = dict()

# std plugins
## type: socket
import instrument_server.device.socket
register_plugin('instrument_server.device.socket')
## type: visa
import instrument_server.device.visa
register_plugin('instrument_server.device.visa')
