from   .application import Application
from   .client      import Client
from   .helpers     import is_ipv4
import asyncio
from   asyncio      import start_server


# constants
BUFFER_SIZE  = 1024


class InstrumentServer:
    def __init__(self, plugins, devices):
        self.plugins     = plugins
        self.devices     = devices
        self.server      = None
        self.application = Application(plugins, devices)

    async def serve_forever(self, address, port):
        with self.application:
            await self.start_server_and_serve_forever(address, port)

    def run(self, address, port):
        """starts a new tcp server and serves forever (blocking)"""
        try:
            asyncio.run(self.serve_forever(address, port))
        except KeyboardInterrupt:
            pass

    # helpers

    def print_server_status(self):
        socket = self.server.sockets[0]
        if is_ipv4(socket):
            # print IPv6
            address, port = socket.getsockname()
            print(f'Running on {address}:{port}...')
        else:
            # print IPv6
            print(f'Running on {socket.getsockname()}...')

    async def handle_new_client(self, reader, writer):
        client = Client(self.application, writer.write)
        while data := await reader.read(BUFFER_SIZE):
            client.receive(data)

    async def start_server(self, address, port):
        """returns a new asyncio tcp server coroutine"""
        server = self.server = await start_server(self.handle_new_client, address, port)
        self.print_server_status()
        return server

    async def start_server_and_serve_forever(self, address, port):
        server = await self.start_server(address, port)
        await server.serve_forever()
