from   instrument_server.device import Base
import socket

BUFFER_SIZE = 1024
class Socket(Base):
    def __init__(self, address, port, timeout=2):
        self.socket = socket.socket()
        self.socket.connect((address, port))
        self.socket.settimeout(timeout)
        self.termchar = b'\n'
    def __del__(self):
        if self.socket:
            self.close()
    def read(self):
        result = self.socket.recv(BUFFER_SIZE)
        while not result.endswith(self.termchar):
            result += self.socket.recv(BUFFER_SIZE)
        return result[:-1]
    def write(self, bytes):
        self.socket.sendall(bytes + self.termchar)
    def close(self):
        self.socket.close()

IS_DEVICE_PLUGIN = True
plugin_name      = 'socket'
plugin           = Socket
