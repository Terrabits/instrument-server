from   .delay_plugin import DelayPlugin
from   importlib     import import_module
from   pathlib       import Path

class CommandError(Exception):
    pass

def register_plugin(module, config={}):
    try:
        if type(module) == str:
            module = import_module(module)
        if not is_plugin(module):
            return False
        if not module.plugin in [i.plugin for i in plugins]:
            plugins.append(DelayPlugin(module.plugin, **config))
        return True
    except:
        return False
def remove_plugin(cls):
    is_not_cls = lambda i: i != cls
    plugins    = list(filter(is_not_cls, plugins))

def is_plugin(module):
    try:
        module.IS_COMMAND_PLUGIN
        return True
    except:
        return False
def get_plugin_pair(module):
    assert is_plugin(module)
    return module.plugin_name, module.plugin

def py_files_in_path(path):
    return [i for i in path.iterdir() if i.is_file() and i.suffix == '.py']
def find_command_plugins():
    device_plugin_path = Path(__file__).parent
    py_files = py_files_in_path(device_plugin_path)
    for py_file in py_files:
        if str(py_file) == __file__:
            continue
        try:
            module_name = str(py_file.name[:-3])
            module = import_module(f'.{module_name}', 'instrument_server.command')
            register_plugin(module)
        except:
            continue

# plugins
plugins = list()

# std plugins
## __quit__
import instrument_server.command.quit
register_plugin('instrument_server.command.error')
register_plugin('instrument_server.command.quit')
