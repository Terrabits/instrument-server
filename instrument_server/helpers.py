from socket import AddressFamily


def is_ipv4(socket):
    if socket.family == AddressFamily.AF_UNIX:
        # unix socket
        return False

    if socket.family == AddressFamily.AF_INET6:
        # IP v6
        return False

    return socket.family == AddressFamily.AF_INET
