import argparse
import socket

parser = argparse.ArgumentParser(description="client connection test for instrument_server")
parser.add_argument('--port', type=int, required=True)
args = parser.parse_args()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', args.port))
s.settimeout(10)

s.sendall(b'is_znb? znb\n')
print(f'is_znb? {s.recv(1024).strip().decode()}')

s.sendall(b'init\n')
s.sendall(b'start_sweeps 10\n')
s.sendall(b'sweep_finished?\n')
print(f'sweep_finished? {s.recv(1024).strip().decode()}')

s.sendall(b'data?\n')
print(f'data? => {s.recv(10000).strip().decode()}')

s.sendall(b'error?\n')
print(f'error? => {s.recv(1024).strip().decode()}')

# Try a native ZNB command
s.sendall(b'*OPT?\n')
print(f"OPT?: '{s.recv(1024).strip().decode()}'")

s.sendall(b'local\n')
s.sendall(b'__quit__\n')
