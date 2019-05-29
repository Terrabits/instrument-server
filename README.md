# instrument Server

TCP server for controlling multiple instruments via a simplified SCPI interface

## Requirements

- python 3.7+
- `ddt` testing package
- `ruamel.yaml` yaml parser package

## Install Requirements

To get started:

```shell
# git clone instrument-server
cd path/to/instrument-server
pip install .
```

Or, alternatively, for development:

```shell
cd path/to/instrument-server
pip install -e .[dev]
```

## Start Server

A command line command `instrument-server` is installed on your system. See `instrument-server --help` for details.

## Example

See `doc/example` for a simple example to help get started.
