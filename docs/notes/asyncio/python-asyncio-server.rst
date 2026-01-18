.. meta::
    :description lang=en: Python asyncio networking - TCP/UDP servers, HTTP clients, SSL/TLS, protocols
    :keywords: Python, Python3, Asyncio, TCP Server, UDP Server, HTTP Client, SSL TLS, Network Programming

===================
Asyncio Networking
===================

:Source: `src/basic/asyncio_.py <https://github.com/crazyguitar/pysheeet/blob/master/src/basic/asyncio_.py>`_

.. contents:: Table of Contents
    :backlinks: none

Introduction
------------

Asyncio excels at network programming because network I/O is inherently
asynchronous - you send a request and wait for a response. Instead of blocking
a thread while waiting, asyncio allows other tasks to run. This section covers
building TCP/UDP servers and clients, HTTP requests, SSL/TLS encryption, and
the Transport/Protocol API for low-level control.

TCP Echo Server with Streams
----------------------------

The streams API (``asyncio.start_server``, ``open_connection``) provides a
high-level interface for TCP networking. It handles buffering, encoding, and
connection management automatically, making it the recommended approach for
most applications.

.. code-block:: python

    import asyncio

    async def handle_client(reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"Connected: {addr}")

        while True:
            data = await reader.read(1024)
            if not data:
                break
            message = data.decode()
            print(f"Received: {message!r} from {addr}")
            writer.write(data)
            await writer.drain()

        print(f"Disconnected: {addr}")
        writer.close()
        await writer.wait_closed()

    async def main():
        server = await asyncio.start_server(
            handle_client, 'localhost', 8888
        )
        addr = server.sockets[0].getsockname()
        print(f"Serving on {addr}")

        async with server:
            await server.serve_forever()

    asyncio.run(main())

TCP Client with Streams
-----------------------

The client side uses ``asyncio.open_connection()`` to establish a connection.
The returned reader and writer objects provide async methods for sending and
receiving data.

.. code-block:: python

    import asyncio

    async def tcp_client(message):
        reader, writer = await asyncio.open_connection(
            'localhost', 8888
        )

        print(f"Sending: {message!r}")
        writer.write(message.encode())
        await writer.drain()

        data = await reader.read(1024)
        print(f"Received: {data.decode()!r}")

        writer.close()
        await writer.wait_closed()

    asyncio.run(tcp_client("Hello, Server!"))

Low-Level TCP with Sockets
--------------------------

For more control, you can use raw sockets with the event loop's socket methods.
This approach is useful when you need fine-grained control over socket options
or when integrating with existing socket-based code.

.. code-block:: python

    import asyncio
    import socket

    async def handle_client(loop, conn):
        while True:
            data = await loop.sock_recv(conn, 1024)
            if not data:
                break
            await loop.sock_sendall(conn, data)
        conn.close()

    async def server():
        loop = asyncio.get_event_loop()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setblocking(False)
        sock.bind(('localhost', 8888))
        sock.listen(100)

        print("Server listening on localhost:8888")
        while True:
            conn, addr = await loop.sock_accept(sock)
            print(f"Connected: {addr}")
            asyncio.create_task(handle_client(loop, conn))

    asyncio.run(server())

UDP Echo Server
---------------

UDP is connectionless, so the API is different from TCP. Use
``create_datagram_endpoint()`` with a protocol class to handle UDP packets.
Each packet is independent and may arrive out of order or not at all.

.. code-block:: python

    import asyncio

    class EchoUDPProtocol(asyncio.DatagramProtocol):
        def connection_made(self, transport):
            self.transport = transport

        def datagram_received(self, data, addr):
            message = data.decode()
            print(f"Received {message!r} from {addr}")
            self.transport.sendto(data, addr)

    async def main():
        loop = asyncio.get_event_loop()
        transport, protocol = await loop.create_datagram_endpoint(
            EchoUDPProtocol,
            local_addr=('localhost', 9999)
        )
        print("UDP server listening on localhost:9999")

        try:
            await asyncio.sleep(3600)  # Run for 1 hour
        finally:
            transport.close()

    asyncio.run(main())

HTTP Client with SSL
--------------------

Making HTTPS requests requires SSL context configuration. This example shows
how to fetch web pages using low-level streams with proper SSL verification.

.. code-block:: python

    import asyncio
    import ssl

    async def fetch_https(host, path="/"):
        # Create SSL context with certificate verification
        ctx = ssl.create_default_context()

        reader, writer = await asyncio.open_connection(
            host, 443, ssl=ctx
        )

        # Send HTTP request
        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        writer.write(request.encode())
        await writer.drain()

        # Read response
        response = await reader.read()
        writer.close()
        await writer.wait_closed()

        return response.decode()

    async def main():
        urls = [
            ("www.python.org", "/"),
            ("github.com", "/"),
        ]
        tasks = [fetch_https(host, path) for host, path in urls]
        responses = await asyncio.gather(*tasks)

        for (host, _), resp in zip(urls, responses):
            status = resp.split('\r\n')[0]
            print(f"{host}: {status}")

    asyncio.run(main())

HTTPS Server with SSL
---------------------

Creating an HTTPS server requires SSL certificates. This example shows a
simple HTTPS server that serves static content with TLS encryption.

.. code-block:: python

    import asyncio
    import ssl

    async def handle_request(reader, writer):
        request = await reader.read(1024)

        response = b"HTTP/1.1 200 OK\r\n"
        response += b"Content-Type: text/html\r\n\r\n"
        response += b"<html><body><h1>Hello HTTPS!</h1></body></html>"

        writer.write(response)
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    async def main():
        # Create SSL context
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain('cert.pem', 'key.pem')

        server = await asyncio.start_server(
            handle_request, 'localhost', 8443, ssl=ctx
        )
        print("HTTPS server on https://localhost:8443")

        async with server:
            await server.serve_forever()

    # Generate self-signed cert:
    # openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
    asyncio.run(main())

Transport and Protocol API
--------------------------

The Transport/Protocol API provides low-level control over network connections.
Transports handle the actual I/O while Protocols handle the data processing.
This separation allows for flexible and reusable network code.

.. code-block:: python

    import asyncio

    class EchoProtocol(asyncio.Protocol):
        def connection_made(self, transport):
            self.transport = transport
            peername = transport.get_extra_info('peername')
            print(f"Connection from {peername}")

        def data_received(self, data):
            print(f"Received: {data.decode()!r}")
            self.transport.write(data)

        def connection_lost(self, exc):
            print("Connection closed")

    async def main():
        loop = asyncio.get_event_loop()
        server = await loop.create_server(
            EchoProtocol, 'localhost', 8888
        )

        async with server:
            await server.serve_forever()

    asyncio.run(main())

DNS Resolution
--------------

Asyncio provides async DNS resolution through ``getaddrinfo()``. This is
useful when you need to resolve hostnames without blocking the event loop.

.. code-block:: python

    import asyncio
    import socket

    async def resolve_host(host, port=80):
        loop = asyncio.get_event_loop()
        infos = await loop.getaddrinfo(
            host, port,
            family=socket.AF_UNSPEC,
            type=socket.SOCK_STREAM
        )

        for family, type_, proto, canonname, sockaddr in infos:
            ip, port = sockaddr[:2]
            family_name = "IPv4" if family == socket.AF_INET else "IPv6"
            print(f"{host} -> {ip} ({family_name})")

    async def main():
        hosts = ["python.org", "github.com", "google.com"]
        await asyncio.gather(*[resolve_host(h) for h in hosts])

    asyncio.run(main())

Simple HTTP Server
------------------

A minimal HTTP server implementation showing how to parse requests and
send responses. For production use, consider frameworks like aiohttp or
FastAPI.

.. code-block:: python

    import asyncio

    async def handle_http(reader, writer):
        request = await reader.read(1024)
        request_line = request.decode().split('\r\n')[0]
        method, path, _ = request_line.split(' ')

        print(f"{method} {path}")

        # Simple routing
        if path == '/':
            body = b"<h1>Home</h1>"
            status = "200 OK"
        elif path == '/about':
            body = b"<h1>About</h1>"
            status = "200 OK"
        else:
            body = b"<h1>404 Not Found</h1>"
            status = "404 Not Found"

        response = f"HTTP/1.1 {status}\r\n"
        response += f"Content-Length: {len(body)}\r\n"
        response += "Content-Type: text/html\r\n\r\n"

        writer.write(response.encode() + body)
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    async def main():
        server = await asyncio.start_server(
            handle_http, 'localhost', 8080
        )
        print("HTTP server on http://localhost:8080")

        async with server:
            await server.serve_forever()

    asyncio.run(main())

Using sendfile for Efficient File Transfer
------------------------------------------

The ``sendfile()`` method (Python 3.7+) efficiently transfers file contents
to a transport using the OS's sendfile syscall, avoiding copying data through
Python.

.. code-block:: python

    import asyncio

    async def handle_request(reader, writer):
        await reader.read(1024)  # Read request

        with open('index.html', 'rb') as f:
            # Get file size
            f.seek(0, 2)
            size = f.tell()
            f.seek(0)

            # Send headers
            headers = f"HTTP/1.1 200 OK\r\n"
            headers += f"Content-Length: {size}\r\n"
            headers += "Content-Type: text/html\r\n\r\n"
            writer.write(headers.encode())

            # Send file efficiently
            loop = asyncio.get_event_loop()
            await loop.sendfile(writer.transport, f)

        writer.close()
        await writer.wait_closed()

    async def main():
        server = await asyncio.start_server(
            handle_request, 'localhost', 8080
        )
        async with server:
            await server.serve_forever()

    asyncio.run(main())

Connection Pool
---------------

Connection pools reuse connections to avoid the overhead of establishing
new connections for each request. This is essential for high-performance
clients that make many requests to the same server.

.. code-block:: python

    import asyncio
    from collections import deque

    class ConnectionPool:
        def __init__(self, host, port, size=5):
            self.host = host
            self.port = port
            self.size = size
            self._pool = deque()
            self._lock = asyncio.Lock()

        async def get(self):
            async with self._lock:
                if self._pool:
                    return self._pool.popleft()

            # Create new connection
            reader, writer = await asyncio.open_connection(
                self.host, self.port
            )
            return reader, writer

        async def put(self, reader, writer):
            async with self._lock:
                if len(self._pool) < self.size:
                    self._pool.append((reader, writer))
                else:
                    writer.close()
                    await writer.wait_closed()

        async def close(self):
            async with self._lock:
                while self._pool:
                    reader, writer = self._pool.popleft()
                    writer.close()
                    await writer.wait_closed()

    async def fetch(pool, message):
        reader, writer = await pool.get()
        try:
            writer.write(message.encode())
            await writer.drain()
            data = await reader.read(1024)
            return data.decode()
        finally:
            await pool.put(reader, writer)

    async def main():
        pool = ConnectionPool('localhost', 8888, size=3)
        try:
            tasks = [fetch(pool, f"msg{i}") for i in range(10)]
            results = await asyncio.gather(*tasks)
            for r in results:
                print(r)
        finally:
            await pool.close()

    asyncio.run(main())
