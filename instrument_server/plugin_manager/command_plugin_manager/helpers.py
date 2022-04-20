def is_plugin(module):
    try:
        module.IS_COMMAND_PLUGIN
        return True
    except:
        return False
