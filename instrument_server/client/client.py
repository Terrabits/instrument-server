from .command_parser import CommandParser
from .helpers        import to_bytes


# constants
BUFFER_SIZE = 1024


class Client:
    def __init__(self, reader, writer, execute_fn):
        self.reader     = reader
        self.writer     = writer
        self.execute_fn = execute_fn
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

    async def serve_forever_and_close(self):
        try:
            await self.serve_forever()
        finally:
            self.writer.close()
            await self.writer.wait_closed()

    def close(self):
        if not self.reader.is_eof():
            self.reader.feed_eof()


    # helpers

    def execute(self, command):
        result = self.execute_fn(command)
        if result is not None:
            assert isinstance(result, bytes)
            self.writer.write(result)

    async def read(self):
        return await self.reader.read(BUFFER_SIZE)

    async def serve_forever(self):
        while data := await self.read():
            self.command_parser.receive(data)
            while command := self.command_parser.next():
                self.execute(command)
