import argparse
import os
from   pathlib import Path
import instrument_server
import sys

def main():
    parser = argparse.ArgumentParser(description='TCP server for controlling multiple instruments via a simplified SCPI interface')
    parser.add_argument('config_filename')
    parser.add_argument('--address',     '-a', type=str, default='0.0.0.0')
    parser.add_argument('--port',        '-p', type=int, default=0)
    parser.add_argument('--termination', '-t', type=str, default='\n')
    parser.add_argument('--debug-mode',  '-d', action='store_true')
    args = parser.parse_args()
    args.termination = args.termination.encode()

    config_path = str(Path(args.config_filename).resolve().parent)
    sys.path.insert(0, os.getcwd())
    sys.path.insert(0, config_path)
    instrument_server.run(**args.__dict__)
    sys.exit(0)

if __name__ == '__main__':
    main()
