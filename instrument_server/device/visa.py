from   instrument_server.device import Base
import pyvisa             as     visa

class Visa(Base):
    def __init__(self, resource_str, open_timeout=visa.constants.VI_TMO_IMMEDIATE, timeout=2000):
        rm                 = visa.ResourceManager()
        self.instr         = rm.open_resource(resource_str, open_timeout=open_timeout)
        self.instr.time_ms = timeout
    def __del__(self):
        if self.instr:
            self.close()
    def read(self):
        return self.instr.read()
    def write(self, bytes):
        self.instr.write(bytes)
    def close(self):
        self.instr.close()

IS_DEVICE_PLUGIN = True
plugin_name      = 'visa'
plugin           = Visa
