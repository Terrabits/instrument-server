from .helpers         import ellipsis_bytes, to_bytes
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
        self.errors       = []

        # add error handling
        errors_command = ErrorsCommand(self.errors)
        self.commands.append(errors_command)

        # add built-ins
        plugins = plugins.copy()
        plugins.append('instrument_server.commands.quit_command')
        plugins.append('instrument_server.devices.socket_factory')
        plugins.append('instrument_server.devices.visa_factory')

        # start
        self.load_plugins(plugins)
        self.open_devices(devices)

    def execute(self, command_bytes):
        assert isinstance(command_bytes, bytes)
        for command in self.commands:
            if not command.is_match(command_bytes):
                continue

            try:
                result = command.execute(self.devices, command_bytes)
                return to_bytes(result)
            except Exception as error:
                # convert exceptions to errors
                print(error, flush=True)
                self.errors.append(error)
                return

        # error: command not found
        message = f"command '{ellipsis_bytes(command_bytes)}' not found"
        error   = CommandNotFoundError(message)
        print(error, flush=True)
        self.errors.append(error)

    def close(self):
        self.close_devices()


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

                message = f"type not found for device '{name}'"
                raise OpenDeviceError(message)

            # type, factory
            device_type = settings.pop('type')
            factory     = self.device_factories[device_type]

            # open
            try:
                device = factory.open(**settings)
            except BaseException as error:
                self.close_devices()

                # reraise
                message = f'{type(error)} error: {error}'
                new_error = OpenDeviceError(message)
                raise new_error from error

            # save
            self.devices     [name] = device
            self.device_types[name] = device_type

    def close_devices(self):
        for name, device in self.devices.items():
            # type and factory
            type    = self.device_types[name]
            factory = self.device_factories[type]

            # close
            factory.close(device)
