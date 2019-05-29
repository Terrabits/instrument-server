from instrument_server.device import Base

class Test(Base):
    def __init__(self, reads=[]):
        self.reads  = reads
        self.writes = []
    def read(self):
        return self.reads.pop(0)
    def write(self, bytes):
        self.writes.append(bytes)
