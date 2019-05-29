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
        assert not name in plugins
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

def py_files_in_path(path):
    return [i for i in path.iterdir() if i.is_file() and i.suffix == '.py']
def find_device_plugins():
    device_plugin_path = Path(__file__).parent
    py_files = py_files_in_path(device_plugin_path)
    for py_file in py_files:
        if str(py_file) == __file__:
            continue
        try:
            module_name = str(py_file.name[:-3])
            module = import_module(f'.{module_name}', 'instrument_server.device')
            register_plugin(module)
        except:
            continue

try:
    plugins
except:
    plugins = dict()
    find_device_plugins()
