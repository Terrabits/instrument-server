import instrument_server
from   instrument_server.command import            Translation
from   instrument_server.command import plugins as command_plugins
from   instrument_server.device  import plugins as device_plugins
from   ruamel              import            yaml
import sys

class CommandNotFoundError(LookupError):
    pass

class Executor(object):
    def __init__(self, config_filename, debug_mode=False):
        self.config_filename = config_filename
        self.debug_mode      = debug_mode
        with open(config_filename, 'r') as f:
            config = yaml.safe_load(f.read())
        self._process_plugins(config.pop('plugins'))
        self._connect_devices(config.pop('devices'))
        self._process_commands(config)
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
