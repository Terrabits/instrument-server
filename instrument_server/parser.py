class Parser(object):
    def __init__(self, initial_buffer=b'', termination=b'\n'):
        self.data = initial_buffer.lstrip()
        self.termination = termination
    def clear(self):
        self.data = b''
    def append(self, data):
        self.data += data
        self.data = self.data.lstrip()
    def is_data(self):
        return bool(self.buffer)
    def next_command(self):
        if not self.data:
            return b''
        i = self.data.find(self.termination)
        if i == -1:
            return b''
        command = self.data[:i].strip()
        self.data    = self.data[i+1:].lstrip()
        if not command:
            return self.next_command()
        else:
            return command
