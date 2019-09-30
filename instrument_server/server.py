from   instrument_server.command  import CommandError
from   instrument_server.device   import DeviceError
from   instrument_server.executor import CommandNotFoundError, Executor
from   instrument_server.parser   import Parser

class Server:
    def __init__(self, config, termination=b'\n', debug_mode=False):
        self.config      = config
        self.debug_mode  = debug_mode
        self.termination = termination
        # executor
        self.executor = Executor(config, debug_mode)

    def new_connection(self):
        return Handler(self.executor, self.termination, self.debug_mode)

class Handler:
    def __init__(self, executor, termination=b'\n', debug_mode=False):
        self.executor    = executor
        self.termination = termination
        self.debug_mode  = debug_mode
        self.parser      = Parser(termination=termination)

    async def handle_read(self, data, send_fn):
        self.parser.append(data)
        command = self.parser.next_command()
        while command:
            try:
                if self.debug_mode:
                    print(command.decode())
                return_value = self.executor.execute(command)
                if return_value != None:
                    if type(return_value) == bytes:
                        await send_fn(return_value + self.termination)
                    else:
                        await send_fn(f'{return_value}'.encode() + self.termination)
            except CommandError as error:
                print(error)
            except DeviceError as error:
                print(error)
            except CommandNotFoundError as error:
                print(error)
            command = self.parser.next_command()
