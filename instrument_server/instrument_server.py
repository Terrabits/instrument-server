from   .application import Application
from   .client      import Client
from   .helpers     import is_ipv4
import asyncio
from   asyncio      import CancelledError, start_server


# constants
BUFFER_SIZE  = 1024


class InstrumentServer:
    def __init__(self, plugins, devices):
        # tcp server
        self.shutdown = False
        self.clients  = []
        self.server   = None

        # app
        self.plugins     = plugins
        self.devices     = devices
        self.application = None

    @property
    def is_running(self):
        return self.server is not None

    async def serve_forever(self, address, port):
        try:
            assert not self.is_running
            self.application = Application(self.plugins, self.devices)
            await self.start_server(address, port)
            self.print_server_status()
            await self.server.serve_forever()
        except CancelledError:
            await self.close_clients()
            self.application.close_devices()
            print('shutdown', flush=True)

    async def stop(self):
        if self.server:
            # remove reference
            server = self.server
            self.server = None

            # close
            server.close()
            await server.wait_closed()

    def run(self, address, port):
        """starts a new tcp server and serves forever (blocking)"""
        assert not self.is_running
        try:
            asyncio.run(self.serve_forever(address, port))
        except SystemExit:
            pass
        except KeyboardInterrupt:
            pass


    # helpers

    def print_server_status(self):
        socket = self.server.sockets[0]
        if is_ipv4(socket):
            # print IPv6
            address, port = socket.getsockname()
            print(f'Running on {address}:{port}...', flush=True)
        else:
            # print IPv6
            print(f'Running on {socket.getsockname()}...', flush=True)

    # client helpers

    def add_client(self, client):
        self.clients.append(client)

    def remove_client(self, client):
        if client not in self.clients:
            return

        # find index
        index = self.clients.index(client)

        # delete by index
        del(self.clients[index])

    async def handle_new_client(self, reader, writer):
        client = Client(self.application, reader, writer)
        self.add_client(client)
        print(f'  connected:    {client}', flush=True)

        # for exception handling
        close_client = False
        shutdown     = False
        error        = None

        try:
            await client.serve_forever()
        except CancelledError:
            # handle client task cancelled
            close_client = True
            shutdown     = False
            # ignore error
        except SystemExit as e:
            # received quit command from client
            close_client = False
            shutdown     = True
            # ignore error
        except BaseException as e:
            # bad stuff happened
            close_client = True
            shutdown     = True
            error        = e

        # close
        self.remove_client(client)
        if close_client:
            await client.close()

        print(f'  disconnected: {client}', flush=True)

        # shut down server?
        if shutdown:
            await self.stop()

        if error:
            raise error

    async def close_clients(self):
        for client in self.clients:
            await client.close()
        self.clients.clear()

    # tcp socket helpers

    async def start_server(self, address, port):
        """returns a new asyncio tcp server coroutine"""
        assert not self.is_running
        self.shutdown = False
        self.server   = await start_server(self.handle_new_client, address, port)
        return self.server
