# Instrument Server Example

This example serves an application-specific protocol via TCP socket for making measurements with a Rohde & Schwarz ZNB Vector Network Analyzer.

## Requirements

- Rohde & Schwarz ZNB Vector Network Analyzer
- Python 3.7+
- `instrument_server` python module installed
- A terminal application

## Protocol

The following commands are defined in `example-config.yaml`:

- `init`
- `start_sweeps <count>`
- `sweep_finished?`
- `data?`
- `error?`
- `local`

For the sake of example, the `is_znb?` command is implemented as a Command plugin.

## Test

`test.py` is a command-line utility that connects to the instrument server and sends a few commands before disconnecting.

The commands sent are:

```shell
is_znb? znb
init
start_sweeps 10
sweep_finished?
data?
error?
local
__quit__
```

The `__quit__` command is built into `instrument-server` and shuts it down.

## Test Instructions

First, make sure that the ZNB is connected via network and make a note of it's IP address. Change the following value in `example-config.yaml`:

```yaml
devices:
  znb:
    type:    socket
    address: <znb ip address>
```

Next, open two terminals.

In terminal 1, execute the following:

```shell
# Terminal 1
cd path/to/instrument-server/doc/example
instrument-server example-config.yaml
```

The output should look something like:

```shell
address 0.0.0.0, port: XXXX
Server accepting connection
```

Make a note of which port instrument-server is listening on.

With terminal 1 still open and instrument-server running, open a second terminal and execute the following:

```shell
# Terminal 2
cd path/to/instrument-server/doc/example
python test.py --port XXXX
```

The result should look something like this:
[Screen capture](example.mov)
