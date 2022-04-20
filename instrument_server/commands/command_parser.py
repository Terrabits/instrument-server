from   .mixins import RaiseErrorMixin
import re


class CommandParser(RaiseErrorMixin):
    def __init__(self, command, args={}):
        RaiseErrorMixin.__init__(self)
        self.command = command
        self.args    = args

    def is_match(self, command_bytes):
        regex = f'^{self.command}\\s*'.replace('?', r'\?').encode()
        matches = re.match(regex, command_bytes)
        return matches is not None

    def parse_args(self, command_bytes):
        values = command_bytes.strip().split()[1:]
        if len(values) < len(self.args):
            self.raise_error('Too few arguments')
        if len(values) > len(self.args):
            self.raise_error('Too many arguments')

        args = {}
        for name, type, value in zip(self.args.keys(), self.args.values(), values):
            if type:
                try:
                    typed_value = type(value)
                except (TypeError, ValueError) as ex:
                    self.raise_error(f"'{value}' is not a valid {type}")
                args[name] = typed_value
            else:
                # decode bytes to str
                args[name] = value.decode()
        return args
