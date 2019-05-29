# to declare device for auto-import.
# See below class definition.

class Comment(Base):
    def __init__(self, **settings):
        pass
    def read(self):
        pass
    def write(self, bytes):
        pass
    def query(self, bytes):
        self.write(bytes)
        return self.read()
    def close(self):
        pass

# # Declare as device plugin
# # for auto-import
# IS_DEVICE_PLUGIN = True
# plugin_name      = 'base'
# plugin           = Base
