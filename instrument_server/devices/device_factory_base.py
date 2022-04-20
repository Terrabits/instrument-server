from .mixins import RaiseErrorMixin
from abc     import ABCMeta, abstractmethod


class DeviceFactoryBase(RaiseErrorMixin, metaclass=ABCMeta):
    @property
    @abstractmethod
    def type(self):
        """device type for reference in devices list"""

    @abstractmethod
    def open(self, **settings):
        """return opened device with `settings`"""

    def close(self, device):
        """close `device`"""
        # device.close()
