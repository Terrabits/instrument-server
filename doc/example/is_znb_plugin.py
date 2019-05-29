from instrument_server.command import Base, CommandError

class IsZnb(Base):
    def is_match(self, received_command):
        parts = received_command.split()
        return parts[0] == b'is_znb?'
    def execute(self, received_command):
        parts = received_command.split()
        if len(parts) != 2:
            raise CommandError("'is_znb' requires one argument: device name")
        name = parts[1].decode()
        device = self.devices[name]
        id = device.query(b'*IDN?')
        return 1 if b'znb' in id.strip().lower() else 0

IS_COMMAND_PLUGIN = True
plugin            = IsZnb
