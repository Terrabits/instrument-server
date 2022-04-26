from socket import AddressFamily


def is_ipv4(socket):
    return socket.family == AddressFamily.AF_INET
