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
        self.commands   = []
        self.config     = None
        self.debug_mode = debug_mode
        self.devices    = dict()
        self.state      = dict()
        self._load_config(config)
        self._process_plugins (self.config.pop('plugins'))
        self._connect_devices (self.config.pop('devices'))
        self._process_translation_commands(self.config)
        self._process_command_plugins()

    def execute(self, received_command):
        for command in self.commands:
            if command.is_match(received_command):
                return command.execute(received_command)
        raise CommandNotFoundError(f'Definition not found for "{received_command}"')

    def _load_config(self, config):
        config_is_filename = type(config) == str
        if config_is_filename:
            self._load_config_from_filename(config)
        else:
            # assume config IS config
            self.config = config
    def _load_config_from_filename(self, filename):
        # add config path to python paths
        path = Path(self.filename).resolve().parent
        sys.path.insert(0, str(path))

        # load yaml
        with open(filename, 'r') as f:
            self.config = yaml.safe_load(f.read())

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
        for name, settings in plugin_list.items():
            if instrument_server.command.register_plugin(name, state, settings):
                continue
            if instrument_server.device.register_plugin(name):
                continue
            # else
            raise ImportError(f"Error importing plugin '{name}'")
    def _process_translation_commands(self, commands):
        translation_commands = []
        for command_definition, outgoing_commands in commands.items():
            command = Translation(command_definition, outgoing_commands, self.devices)
            translation_commands.append(command)
        self.commands += translation_commands
    def _process_command_plugins(self):
        plugin_commands = [plugin(self.devices) for plugin in instrument_server.command.plugins]
        self.commands += plugin_commands
