class DelayPlugin(object):
    def __init__(self, plugin, **settings):
        self.plugin   = plugin
        self.settings = settings
    def __eq__(self, plugin):
        return self.plugin == plugin
    def __call__(self, devices, state):
        return self.plugin(devices, state, **self.settings)
