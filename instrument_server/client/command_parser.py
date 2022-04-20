class CommandParser:
    def __init__(self, initial_data=b'', term_char=b'\n'):
        self.data        = initial_data.lstrip()
        self.term_char = term_char

    def receive(self, data):
        self.data += data
        self.data  = self.data.lstrip()

    def next(self):
        # data?
        if not self.data:
            return None

        # term_char?
        i = self.data.find(self.term_char)
        if i == -1:
            return None

        # parse
        command   = self.data[:i].strip()
        self.data = self.data[i+1:].lstrip()
        return command or self.next_command()
