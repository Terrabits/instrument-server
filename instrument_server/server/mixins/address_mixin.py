from socket import AddressFamily


# constants
IPV4 = AddressFamily.AF_INET


class AddressMixin:
    @property
    def is_ipv4(self):
        return self.socket1.family == IPV4

    @property
    def address(self):
        if self.is_ipv4:
            # sockname = (address, port)
            return self.sockname[0]
        # else
        return self.sockname

    @property
    def port(self):
        assert self.is_ipv4
        # sockname = (address, port)
        return self.sockname[1]


    # helpers

    @property
    def socket1(self):
        assert self.server.sockets
        return self.server.sockets[0]

    @property
    def sockname(self):
        return self.socket1.getsockname()
