from   .application import Application
from   .client      import Client
from   .helpers     import no_clients_running
from   .server      import Server
import asyncio
from   asyncio      import CancelledError, start_server


# constants
BUFFER_SIZE       = 1024
FORGIVABLE_ERRORS = (KeyboardInterrupt, SystemExit)


class InstrumentServer:
    def __init__(self, plugins, devices):
        # tcp
        self.server   = None
        self.clients  = []

        # app
        self.plugins     = plugins
        self.devices     = devices
        self.application = None

    @property
    def is_running(self):
        return self.server is not None

    async def serve_forever_and_close(self, address, port):
        assert not self.is_running
        self.application = Application(self.plugins, self.devices)
        self.server      = Server()
        try:
            await self.server.serve_forever_and_close(self.handle_new_client, address, port)
        except CancelledError:
            pass
        finally:
            self.server = None
            self.close_clients()
            assert no_clients_running()
            self.application.close()

    def close(self):
        assert self.is_running
        self.server.close()

    def run(self, address, port):
        """starts a new tcp server and serves forever (blocking)"""
        assert not self.is_running
        try:
            asyncio.run(self.serve_forever_and_close(address, port))
        except FORGIVABLE_ERRORS:
            pass


    # helpers

    def new_client(self, reader, writer):
        execute_fn = self.application.execute
        client     = Client(reader, writer, execute_fn)
        self.clients.append(client)
        return client

    def remove_client(self, client):
        assert client in self.clients
        index = self.clients.index(client)
        del(self.clients[index])

    async def handle_new_client(self, reader, writer):
        client = self.new_client(reader, writer)
        print(f'  connected:    {client}', flush=True)

        shutdown = False
        try:
            await client.serve_forever()
        except CancelledError:
            pass
        except SystemExit:
            shutdown = True
        finally:
            # client is closed
            self.remove_client(client)
            print(f'  disconnected: {client}', flush=True)
            if shutdown:
                self.close()

    async def close_server_and_wait(self):
        # take reference
        server = self.server
        self.server = None

        # close and wait
        server.close()
        await server.wait_closed()

    def close_clients(self):
        for client in self.clients:
            client.close()
