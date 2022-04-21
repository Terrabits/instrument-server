from instrument_server.errors import DeviceError, OpenDeviceError


class RaiseErrorMixin:
    def raise_open_error(self, message):
        raise OpenDeviceError(f'{self.type} open error: {message}')

    def raise_error(self, message):
        raise DeviceError(f'{self.type} error: {message}')
