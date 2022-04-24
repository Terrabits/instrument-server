from .command_parser import CommandParser
from .helpers        import to_bytes


# constants
BUFFER_SIZE = 1024


class Client:
    def __init__(self, application, reader, writer):
        self.reader      = reader
        self.writer      = writer
        self.application = application
        self.command_parser = CommandParser()

    @property
    def address(self):
        address, _ = self.writer.get_extra_info('peername')
        return address

    @property
    def port(self):
        _, port = self.writer.get_extra_info('peername')
        return port

    def __repr__(self):
        return f'Client({self.address}, {self.port})'

    async def serve_forever(self):
        while data := await self.read():
            self.command_parser.receive(data)
            while command := self.command_parser.next():
                self.execute(command)

    # helpers

    def execute(self, command):
        result = self.application.execute(command)
        if result is not None:
            # query; send result
            self.writer.write(to_bytes(result))

    async def close(self):
        if not self.writer.is_closing:
            self.writer.close()
        await self.writer.wait_closed()

    async def read(self):
        return await self.reader.read(BUFFER_SIZE)
