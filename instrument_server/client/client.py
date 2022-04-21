from .command_parser import CommandParser
from .helpers        import to_bytes


class Client:
    def __init__(self, application, write_fn, term_char=b'\n'):
        # client connection
        self.application    = application
        self.write          = write_fn
        self.term_char      = term_char
        self.command_parser = CommandParser(term_char=term_char)

    def receive(self, data):
        self.command_parser.receive(data)
        while command := self.command_parser.next():
            self.execute_handle_exceptions(command)


    # helpers

    def execute_handle_exceptions(self, command):
        try:
            result = self.application.execute(command)
        except Exception as error:
            print(error)
            self.application.error_queue.append(error)

        if result:
            # send to client
            self.write(to_bytes(result))
