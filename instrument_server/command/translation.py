from instrument_server.command import Base, CommandError

# replaces {arg}
# with kwargs_dict[arg]
class Formatter(object):
    def __init__(self, arg_names, arg_values):
        self.kwargs = self.to_kwargs(arg_names, arg_values)
    def format(self, command):
        return command.format_map(self.kwargs)
    @staticmethod
    def to_kwargs(names, values):
        kwargs_dict = dict()
        for i in range(0, len(values)):
            kwargs_dict[names[i]] = values[i]
        return kwargs_dict

class Translation(object):
    def __init__(self, command_definition, outgoing_commands, devices):
        parts = command_definition.split()
        self.command    = parts[0 ].lower()
        self.arg_names  = parts[1:]
        self.outgoing_commands = outgoing_commands
        self.devices    = devices
    @property
    def is_query(self):
        return self.command.endswith('?')

    def is_match(self, command):
        return command.decode().split()[0].lower() == self.command
    def execute(self, received_command):
        assert self.is_match(received_command)
        arg_values = [i.decode() for i in received_command.split()[1:]]
        if not self.arg_names and arg_values:
            raise CommandError(f"'{self.command}' has no arguments")
        if len(self.arg_names) > len(arg_values):
            raise CommandError(f"'{self.command}': too few arguments")
        if len(self.arg_names) < len(arg_values):
            raise CommandError(f"'{self.command}': too many arguments")

        last_device = None
        formatter = Formatter(self.arg_names, arg_values)
        for i in self.outgoing_commands:
            device_name, command = list(i.items())[0]
            device  = self.devices[device_name]
            command = formatter.format(command)
            device.write(command.encode())
            last_device = device
        if self.is_query:
            return last_device.read()
    @property
    def help_str(self):
        return f'{self.command} {" ".join(self.arg_names)}'
