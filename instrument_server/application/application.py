from .helpers         import ellipsis_bytes
from ..commands       import ErrorsCommand
from ..plugin_manager import PluginManager
from ..errors         import CommandNotFoundError, OpenDeviceError


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

        # built-ins
        plugins.append('instrument_server.commands.quit_command')
        plugins.append('instrument_server.devices.socket_factory')
        plugins.append('instrument_server.devices.visa_factory')

        # start
        self.load_plugins(plugins)
        try:  # open devices, catch BaseException
            self.open_devices(devices)
        except BaseException as error:
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
                try:  # execute command, catch Exception
                    return command.execute(self.devices, command_bytes)
                except Exception as error:
                    # log non-exiting error
                    print(error, flush=True)
                    self.errors.append(error)
                    return

        # error: command not found
        message = f"command '{ellipsis_bytes(command_bytes)}' not found"
        error   = CommandNotFoundError(message)
        print(error, flush=True)
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
