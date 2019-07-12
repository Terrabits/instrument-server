from instrument_server.command import Base

class PassThru(Base):
    def is_match(self, received_command):
        return True
    def execute(self, received_command):
        print(f'passing {received_command}')
        if 'device' in self.settings:
            name   = self.settings['device']
            device = self.devices[name]
        else:
            device = list(self.devices.values())[0]
        if received_command.strip().endswith(b'?'):
            return device.query(received_command)
        # else
        device.write(received_command)

IS_COMMAND_PLUGIN = True
plugin            = PassThru
print('passthru_plugin imported')
