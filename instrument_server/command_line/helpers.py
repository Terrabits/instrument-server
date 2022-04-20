def prog_for(app_name):
    return app_name.strip().replace(' ', '-')


def description_for(app_name):
    f'command line tool for starting {app_name}'
