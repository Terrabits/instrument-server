def is_plugin(module):
    try:  # IS_COMMAND_PLUGIN?
        module.IS_COMMAND_PLUGIN
        return True
    except:
        return False
