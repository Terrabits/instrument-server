# Instrument Server

Instrument Server is a framework for creating Test & Measurement (T&M) application microservices.

## Requirements

- `python` ~= 3.7
- `ruamel.yaml` ~= 0.15.85
- `pyvisa` ~= 1.9.1

## Install

Instrument Server is available on PyPi:

[instrument-server](https://pypi.org/project/instrument-server/)

It can be installed as expected via pip:

```shell
pip install instrument-server
```

## Command Line Interface

The `instrument-server` python package provides a Command Line Interface (CLI) for starting and stopping Instrument Servers.

From `--help`:

```comment
usage: instrument-server [-h] [--address ADDRESS] [--port PORT]
                         [--termination TERMINATION] [--debug-mode]
                         config_filename

Command Line Interface for starting Instrument Server microservices

positional arguments:
  config_filename

optional arguments:
  -h, --help            show this help message and exit
  --address ADDRESS, -a ADDRESS
                        Set listening address. Default: 0.0.0.0
  --port PORT, -p PORT  Set listening port. Default: random
  --termination TERMINATION, -t TERMINATION
                        Set the termination character. Default: "\n"
  --debug-mode, -d      print debug info to stdout
```

## Hello World

For a quick introduction to creating `instrument-server` microservices, see:

[Instrument Server Hello World](https://github.com/Terrabits/instrument-server-hello-world)
