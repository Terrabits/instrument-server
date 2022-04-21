from   .helpers            import description_for, prog_for
from   ..instrument_server import InstrumentServer
from   ..yaml              import load_yaml
import argparse
import os
import sys


def main(app_name, plugins=None, devices=None):
    """Instrument Server Application Command Line Interface"""
    parser = argparse.ArgumentParser(prog=prog_for(app_name), description=description_for(app_name))
    parser.add_argument('--address', '-a', type=str, default='0.0.0.0', help='Listening address. Default: 0.0.0.0')
    parser.add_argument('--port',    '-p', type=int, default=9000,      help='Listening port. Default: 9000')
    if plugins is None:
        parser.add_argument('plugins_list_file', type=load_yaml, help='Plugins list file (yaml)')
    if devices is None:
        # require device file
        parser.add_argument('devices_file', type=load_yaml, help='Device connection file (yaml)')

    # parse
    args    = parser.parse_args()
    address = args.address
    port    = args.port
    plugins = plugins if plugins is not None else args.plugins_list_file
    devices = devices if devices is not None else args.devices_file

    # plugins list?
    if not isinstance(plugins, list):
        message = 'plugins must be list of modules'
        raise TypeError(message)

    # devices dict?
    if not isinstance(devices, dict):
        message = 'devices must be dict of device declarations'
        raise TypeError(message)

    # import plugins from the
    # current working directory
    sys.path.insert(0, os.getcwd())

    # run
    server = InstrumentServer(plugins, devices)
    server.run(address, port)
    sys.exit(0)
