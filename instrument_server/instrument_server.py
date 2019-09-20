from   .server import Server
import asyncio
from   asyncio import start_server

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
    server  = Server(*args, **kwargs)
    handler = create_handler(server)
    loop    = asyncio.get_event_loop()
    tcp_server    = loop.run_until_complete(start_server(handler, address, port))
    address, port = tcp_server.sockets[0].getsockname()
    print(f'Running on {address}:{port}...')
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        tcp_server.close()
        loop.run_until_complete(tcp_server.wait_closed())
        loop.close()
