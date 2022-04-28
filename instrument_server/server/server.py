from   .mixins import AddressMixin
from   asyncio import start_server
from   socket  import AddressFamily


class Server(AddressMixin):
    def __init__(self):
        self.server = None

    @property
    def exists(self):
        return self.server is not None

    @property
    def is_running(self):
        return self.exists and self.server.is_serving()

    async def serve_forever_and_close(self, handle_client_callback, address, port):
        assert not self.exists
        self.server = await self.start_new_server(handle_client_callback, address, port)
        self.print_status()
        try:
            await self.server.serve_forever()
        finally:
            await self.close_and_wait()
            print('shutdown', flush=True)

    def close(self):
        assert self.is_running
        self.server.close()


    # helpers

    def print_status(self):
        if self.is_ipv4:
            print(f'Serving address {self.address} on port {self.port}...', flush=True)
        else:
            address_str = self.address
            print(f'Serving address {self.address}...', flush=True)

    async def start_new_server(self, handle_client_callback, address, port):
        server = await start_server(handle_client_callback, address, port)
        await server.start_serving()
        return server

    async def close_and_wait(self):
        server      = self.server
        self.server = None
        server.close()
        await server.wait_closed()
