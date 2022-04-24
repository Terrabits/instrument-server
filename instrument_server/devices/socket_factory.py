from .device_factory_base     import DeviceFactoryBase
from instrument_server.errors import DeviceError
from socket                   import socket


# constants
DEFAULT_PORT      = 5025
DEFAULT_TIMEOUT_S = 2.0


class SocketFactory(DeviceFactoryBase):
    type = 'socket'

    def open(self, **settings):
        # is address?
        if 'address' not in settings:
            message = "'address' missing in open()"
            self.raise_open_error(message)

        # get settings
        address   = settings['address']
        port      = settings.get('port', DEFAULT_PORT)
        timeout_s = settings.get('timeout_s', DEFAULT_TIMEOUT_S)

        # new socket
        device = socket()

        # open and return
        try:  # socket.connect, catch Exception
            device.connect((address, port))
        except Exception as error:
            device.close()
            raise error

        # connected
        device.settimeout(timeout_s)
        return device

    def close(self, device):
        device.close()


# export
IS_DEVICE_PLUGIN = True
plugin           = SocketFactory
