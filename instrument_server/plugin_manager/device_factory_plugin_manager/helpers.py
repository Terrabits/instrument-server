def is_plugin(module):
    try:  # IS_DEVICE_PLUGIN
        module.IS_DEVICE_PLUGIN
        return True
    except:
        return False
