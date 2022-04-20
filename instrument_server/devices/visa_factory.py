from .device_factory_base     import DeviceFactoryBase
from instrument_server.errors import DeviceError
from pyvisa                   import ResourceManager
from pyvisa.resources         import Resource


# constants
DEFAULT_TIMEOUT_S = 5.0


class VisaFactory(DeviceFactoryBase):
    type = 'visa'

    @staticmethod
    def open(**settings):
        # resource_str?
        if 'resource_str' not in settings:
            message = "'resource_str' is missing in open()"
            self.raise_open_error(message)

        # settings
        resource_str = settings['resource_str']
        timeout_s    = settings.get('timeout_s', DEFAULT_TIMEOUT_S)

        manager = ResourceManager()
        device  = manager.open_resource(resource_str, open_timeout=timeout_s)
        device.time_ms = timeout_s
        return device

    @staticmethod
    def close(device):
        device.close()


# export
IS_DEVICE_PLUGIN = True
plugin           = VisaFactory
