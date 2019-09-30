from   .server import Server
import asyncio
from   asyncio import start_server
from   socket  import AddressFamily

def ipv4_sockets_from(sockets):
    return [i for i in sockets if i.family != AddressFamily.AF_INET6]

def create_handler(server):
    async def handler(reader, writer):
        async def send_fn(data):
            writer.write(data)
        handler = server.new_connection()
        while True:
            data = await reader.read(1024)
            await handler.handle_read(data, send_fn)
        writer.close()
    return handler

def run(address='0.0.0.0', port=None, *args, **kwargs):
    async def main():
        server       = Server(*args, **kwargs)
        handler      = create_handler(server)
        tcp_server   = await start_server(handler, address, port)
        ipv4_sockets = ipv4_sockets_from(tcp_server.sockets)
        if ipv4_sockets:
            _addr, _port = tcp_server.sockets[0].getsockname()
            print(f'Running on {_addr}:{_port}...')
        else:
            sockname = tcp_server.sockets[0].getsockname()
            print(f'Running on {sockname}')
        async with tcp_server:
            await tcp_server.serve_forever()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
