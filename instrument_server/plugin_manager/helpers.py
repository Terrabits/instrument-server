from importlib import import_module


def load_module(module):
        if type(module) == str:
            module = import_module(module)
        return module
