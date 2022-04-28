from instrument_server.devices import DeviceFactoryBase


class DeviceFactory(DeviceFactoryBase):
    type = 'device1'

    def open(self, **settings):
        return object()

    def close(self, device):
        pass


# export
IS_DEVICE_PLUGIN = True
plugin            = DeviceFactory
