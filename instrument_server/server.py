import asyncio
from   instrument_server.command  import CommandError
from   instrument_server.device   import DeviceError
from   instrument_server.executor import CommandNotFoundError, Executor
from   instrument_server.parser   import Parser
import signal
import socket
import sys
import websockets

def sys_exit(*args, **kwargs):
    sys.exit(0)

class Server:
    def __init__(self, config_filename, address='0.0.0.0', port=0, termination=b'\n', debug_mode=False):
        self.config_filename = config_filename
        self.address     = address
        self.port        = port
        self.termination = termination
        self.debug_mode  = debug_mode
        self.executor    = Executor(config_filename, debug_mode)

    async def accept_connection(self, websocket, path):
        print(f'Server accepting connection (path={path})', flush=True)
        handler = Handler(websocket, self.executor, self.termination)
        await handler.read(websocket, path)

    @staticmethod
    def run(*args, **kwargs):
        server = Server(*args, **kwargs)
        signal.signal(signal.SIGTERM, sys_exit)
        try:
            start_server = websockets.serve(server.accept_connection, server.address, server.port)
            asyncio.get_event_loop().run_until_complete(start_server)

            sockname = start_server.ws_server.server.sockets[0].getsockname()
            address  = sockname[0]
            port     = sockname[1]
            print(f'address {address}, port: {port}')
            asyncio.get_event_loop().run_forever()
        except KeyboardInterrupt:
            pass

# BUFFER_SIZE = 1024
class Handler:
    def __init__(self, websocket, executor, termination=b'\n', debug_mode=False):
        self.websocket   = websocket
        self.executor    = executor
        self.termination = termination
        self.debug_mode  = debug_mode
        self.parser      = Parser(termination=termination)
    async def read(self, websocket, path):
        async for message in websocket:
            if type(message) == str:
                message = message.encode()
            self.parser.append(message)
            command = self.parser.next_command()
            while command:
                try:
                    if self.debug_mode:
                        print(command.decode())
                    return_value = self.executor.execute(command)
                    if return_value != None:
                        if type(return_value) == bytes:
                            await self.websocket.send(return_value + self.termination)
                        else:
                            await self.websocket.send(f'{return_value}'.encode() + self.termination)
                except CommandError as error:
                    print(error)
                except DeviceError as error:
                    print(error)
                except CommandNotFoundError as error:
                    print(error)
                command = self.parser.next_command()
