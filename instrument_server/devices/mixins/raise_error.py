from instrument_server.errors import DeviceError, OpenDeviceError


class RaiseErrorMixin:
    def raise_open_error(self, message):
        raise OpenDeviceError(f'OpenDeviceError: {message}')

    def raise_error(self, message):
        raise DeviceError(f'DeviceError: {message}')
