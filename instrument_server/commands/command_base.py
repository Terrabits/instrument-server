from .mixins import RaiseErrorMixin
from abc     import ABCMeta, abstractmethod


class CommandBase(RaiseErrorMixin, metaclass=ABCMeta):
    """Command Plugin base class"""

    @abstractmethod
    def is_match(self, command_bytes):
        """returns `True` if self can execute command; `False` otherwise"""

    @abstractmethod
    def execute(self, devices, command_bytes):
        """executes command (bytes) with devices"""
