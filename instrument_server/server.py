import asyncore
from   instrument_server.command  import CommandError
from   instrument_server.device   import DeviceError
from   instrument_server.executor import CommandNotFoundError, Executor
from   instrument_server.parser   import Parser
import signal
import socket
import sys

def sys_exit(*args, **kwargs):
    sys.exit(0)

class Server(asyncore.dispatcher):
    def __init__(self, config_filename, address='0.0.0.0', port=0, termination=b'\n', debug_mode=False):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind((address, port))
        self.listen(1)
        self.executor    = Executor(config_filename, debug_mode)
        self.debug_mode  = debug_mode
        self.termination = termination
    @property
    def address(self):
        return self.socket.getsockname()[0]
    @property
    def port(self):
        return self.socket.getsockname()[1]
    def handle_accept(self):
        print('Server accepting connection', flush=True)
        sock, addr = self.accept()
        Handler(sock, self.executor, self.termination)
    @staticmethod
    def run(*args, **kwargs):
        server = Server(*args, **kwargs)
        signal.signal(signal.SIGTERM, sys_exit)
        try:
            print(f'address {server.address}, port: {server.port}')
            asyncore.loop()
        except KeyboardInput:
            pass
        finally:
            asyncore.close_all()
            sys.exit(0)

BUFFER_SIZE = 1024
class Handler(asyncore.dispatcher_with_send):
    def __init__(self, sock, executor, termination=b'\n', debug_mode=False):
        asyncore.dispatcher_with_send.__init__(self, sock)
        self.executor      = executor
        self.termination = termination
        self.debug_mode  = debug_mode
        self.parser      = Parser(termination=termination)
    def handle_read(self):
        self.parser.append(self.recv(BUFFER_SIZE))
        command = self.parser.next_command()
        while command:
            try:
                if self.debug_mode:
                    print(command.decode())
                return_value = self.executor.execute(command)
                if return_value != None:
                    if type(return_value) == bytes:
                        self.send(return_value + self.termination)
                    else:
                        self.send(f'{return_value}'.encode() + self.termination)
            except CommandError as error:
                print(error)
            except DeviceError as error:
                print(error)
            except CommandNotFoundError as error:
                print(error)
            command = self.parser.next_command()
