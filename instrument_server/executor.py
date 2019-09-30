import instrument_server
from   instrument_server.command import            Translation
from   instrument_server.command import plugins as command_plugins
from   instrument_server.device  import plugins as device_plugins
from   pathlib                   import Path
from   ruamel                    import yaml
import sys

class CommandNotFoundError(LookupError):
    pass

class Executor(object):
    def __init__(self, config, debug_mode=False):
        self.config     = config
        self.debug_mode = debug_mode
        if type(config) == str:
            # config is filename
            self.config_filename = config
            config_path = Path(self.config_filename).resolve().parent
            sys.path.insert(0, str(config_path))
            with open(self.config_filename, 'r') as f:
                self.config = yaml.safe_load(f.read())
        self._process_plugins (self.config.pop('plugins'))
        self._connect_devices (self.config.pop('devices'))
        self._process_commands(self.config)
    def execute(self, received_command):
        for command in self.commands:
            if command.is_match(received_command):
                return command.execute(received_command)
        raise CommandNotFoundError(f'Definition not found for "{received_command}"')

    def _connect_devices(self, devices):
        self.devices = dict()
        for name in devices:
            config = devices[name]
            type   = config.pop('type')
            self.devices[name] = device_plugins[type](**config)
    @staticmethod
    def _process_plugins(plugin_list):
        if not plugin_list:
            return
        for name, config in plugin_list.items():
            if instrument_server.command.register_plugin(name, config):
                continue
            if instrument_server.device.register_plugin(name):
                continue
            # else
            raise ImportError(f"Error importing plugin '{name}'")
    def _process_commands(self, commands):
        self.commands = []
        for command_definition, outgoing_commands in commands.items():
            command = Translation(command_definition, outgoing_commands, self.devices)
            self.commands.append(command)
        plugins = [plugin(self.devices) for plugin in instrument_server.command.plugins]
        self.commands += plugins
