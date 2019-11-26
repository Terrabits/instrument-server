class DelayPlugin(object):
    def __init__(self, plugin, state, **settings):
        self.plugin   = plugin
        self.state    = state
        self.settings = settings
    def __eq__(self, plugin):
        return self.plugin == plugin
    def __call__(self, devices):
        return self.plugin(devices, self.state, **self.settings)
