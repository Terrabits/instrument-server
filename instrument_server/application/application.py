from instrument_server.commands       import ErrorsCommand
from instrument_server.plugin_manager import PluginManager
from instrument_server.errors         import CommandNotFoundError, OpenDeviceError


class Application:
    def __init__(self, plugins, devices):
        # init plugins
        self.plugins          = PluginManager()
        self.device_factories = dict()
        self.commands         = []

        # init app state
        self.devices      = {}
        self.device_types = {}
        self.errors       = []  # TODO: fix error queue

        # add error handling
        errors_command = ErrorsCommand(self.errors)
        self.commands.append(errors_command)

        # start
        self.load_plugins(plugins)
        try:
            self.open_devices(devices)
        except Exception as error:
            self.close_devices()
            raise error

    def __del__(self):
        self.close_devices()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_devices()

    def execute(self, command_bytes):
        for command in self.commands:
            if command.is_match(command_bytes):
                try:
                    # execute and return result
                    return command.execute(self.devices, command_bytes)
                except Exception as error:
                    print(error)
                    self.errors.append(error)

        # no match
        message = f'Definition not found for {command_bytes}'
        error   = CommandNotFoundError(message)
        print(error)
        self.errors.append(error)

    # helpers

    def load_plugins(self, plugins):
        # register plugins
        self.plugins.register_plugins(plugins)

        # load command plugins
        for Command in self.plugins.commands:
            command_obj = Command()
            self.commands.append(command_obj)

        # load device factory plugins
        for DeviceFactory in self.plugins.device_factories:
            type = DeviceFactory.type
            self.device_factories[type] = DeviceFactory()

    def open_devices(self, devices):
        for name, settings in devices.items():
            if 'type' not in settings:
                self.close_devices()
                message = f"type not found for device {name}"
                raise OpenDeviceError(message)

            # type, factory
            type    = settings.pop('type')
            factory = self.device_factories[type]

            # open and save
            device                  = factory.open(**settings)
            self.devices[name]      = device
            self.device_types[name] = type

    def close_devices(self):
        for name, device in self.devices.items():
            # type and factory
            type    = self.device_types[name]
            factory = self.device_factories[type]

            # close
            factory.close(device)

        # clear all devices
        self.devices.clear()
        self.device_types.clear()
