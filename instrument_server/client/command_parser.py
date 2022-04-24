# constants
TERM_CHAR = b'\n'


class CommandParser:
    def __init__(self, initial_data=b''):
        self.data        = initial_data.lstrip()

    def receive(self, data):
        self.data += data
        self.data  = self.data.lstrip()

    def next(self):
        # data?
        if not self.data:
            return None

        # term char?
        i = self.data.find(TERM_CHAR)
        if i == -1:
            return None

        # parse
        command   = self.data[:i].strip()
        self.data = self.data[i+1:].lstrip()
        return command or self.next_command()
