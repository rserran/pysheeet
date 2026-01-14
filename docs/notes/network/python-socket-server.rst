.. meta::
    :description lang=en: Python TCP and UDP server tutorial with examples for echo servers, IPv6 dual-stack, Unix domain sockets, SocketServer module, threaded servers, and zero-copy sendfile
    :keywords: Python, socket, TCP server, UDP server, echo server, IPv6, dual-stack, Unix domain socket, SocketServer, network programming, threaded server, sendfile, IPC

==============
Socket Servers
==============

.. contents:: Table of Contents
    :backlinks: none

Building network servers is one of the most common applications of socket programming.
A server listens for incoming connections on a specific port, accepts client connections,
and processes requests. Python's socket module provides all the primitives needed to
build robust TCP and UDP servers, from simple single-threaded echo servers to complex
multi-client applications.

This section covers building TCP and UDP servers in Python using the socket module,
including simple echo servers for learning the basics, IPv6 and dual-stack servers
for modern network compatibility, Unix domain sockets for high-performance local IPC,
the SocketServer module for rapid development, threaded servers for handling multiple
clients, and zero-copy file transfer with sendfile. These patterns form the foundation
for building production-ready network services.

Simple TCP Echo Server
----------------------

A basic TCP echo server demonstrates the fundamental server pattern: create a socket,
bind to an address, listen for connections, accept clients, and process data. This
example uses Python's context manager protocol for proper resource cleanup, ensuring
the socket is closed even if an exception occurs. The ``SO_REUSEADDR`` option allows
the server to restart immediately without waiting for the TIME_WAIT state to expire.

.. code-block:: python

    import socket

    class Server:
        def __init__(self, host, port):
            self._host = host
            self._port = port

        def __enter__(self):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((self._host, self._port))
            sock.listen(10)
            self._sock = sock
            return self._sock

        def __exit__(self, *exc_info):
            if exc_info[0]:
                import traceback
                traceback.print_exception(*exc_info)
            self._sock.close()

    if __name__ == '__main__':
        with Server('localhost', 5566) as s:
            while True:
                conn, addr = s.accept()
                msg = conn.recv(1024)
                conn.send(msg)
                conn.close()

Output:

.. code-block:: console

    $ nc localhost 5566
    Hello World
    Hello World

TCP Echo Server via IPv6
------------------------

IPv6 server using ``AF_INET6`` address family. Note the different address tuple
format which includes flow info and scope ID.

.. code-block:: python

    import contextlib
    import socket

    host = "::1"
    port = 5566

    @contextlib.contextmanager
    def server(host, port):
        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            s.listen(10)
            yield s
        finally:
            s.close()

    with server(host, port) as s:
        try:
            while True:
                conn, addr = s.accept()
                msg = conn.recv(1024)
                if msg:
                    conn.send(msg)
                conn.close()
        except KeyboardInterrupt:
            pass

Output:

.. code-block:: bash

    $ python3 ipv6.py &
    $ nc -6 ::1 5566
    Hello IPv6
    Hello IPv6

Dual-Stack Server (IPv4 and IPv6)
---------------------------------

A server that accepts both IPv4 and IPv6 connections by binding to ``::`` and
disabling ``IPV6_V6ONLY``. IPv4 clients appear as IPv4-mapped IPv6 addresses.

.. code-block:: python

    import contextlib
    import socket

    host = "::"
    port = 5566

    @contextlib.contextmanager
    def server(host, port):
        s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
        try:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            s.bind((host, port))
            s.listen(10)
            yield s
        finally:
            s.close()

    with server(host, port) as s:
        try:
            while True:
                conn, addr = s.accept()
                print(f"Connection from: {conn.getpeername()}")
                msg = conn.recv(1024)
                if msg:
                    conn.send(msg)
                conn.close()
        except KeyboardInterrupt:
            pass

Output:

.. code-block:: bash

    $ python3 dual_stack.py &
    $ nc -4 127.0.0.1 5566
    Connection from: ('::ffff:127.0.0.1', 42604, 0, 0)
    Hello IPv4
    Hello IPv4
    $ nc -6 ::1 5566
    Connection from: ('::1', 50882, 0, 0)
    Hello IPv6
    Hello IPv6

TCP Server via SocketServer
---------------------------

The ``socketserver`` module provides a higher-level interface for building servers.
It handles the socket setup and connection management automatically.

.. code-block:: python

    import socketserver

    class EchoHandler(socketserver.BaseRequestHandler):
        def handle(self):
            data = self.request.recv(1024)
            print(f"Client: {self.client_address}")
            self.request.sendall(data)

    if __name__ == '__main__':
        with socketserver.TCPServer(('localhost', 5566), EchoHandler) as server:
            server.serve_forever()

Simple UDP Echo Server
----------------------

UDP servers use ``SOCK_DGRAM`` and don't require connection handling. Each
``recvfrom()`` returns the data and sender address.

.. code-block:: python

    import socket

    class UDPServer:
        def __init__(self, host, port):
            self._host = host
            self._port = port

        def __enter__(self):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((self._host, self._port))
            self._sock = sock
            return sock

        def __exit__(self, *exc_info):
            if exc_info[0]:
                import traceback
                traceback.print_exception(*exc_info)
            self._sock.close()

    if __name__ == '__main__':
        with UDPServer('localhost', 5566) as s:
            while True:
                msg, addr = s.recvfrom(1024)
                s.sendto(msg, addr)

Output:

.. code-block:: console

    $ nc -u localhost 5566
    Hello World
    Hello World

UDP Server via SocketServer
---------------------------

.. code-block:: python

    import socketserver

    class UDPHandler(socketserver.BaseRequestHandler):
        def handle(self):
            data, sock = self.request
            print(f"Client: {self.client_address}")
            sock.sendto(data, self.client_address)

    if __name__ == '__main__':
        with socketserver.UDPServer(('localhost', 5566), UDPHandler) as server:
            server.serve_forever()

UDP Client - Sender
-------------------

Simple UDP client that sends periodic messages.

.. code-block:: python

    import socket
    import time

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = ('localhost', 5566)

    while True:
        sock.sendto(b"Hello\n", host)
        time.sleep(5)

Broadcast UDP Packets
---------------------

Send UDP packets to all hosts on the local network using broadcast address.

.. code-block:: python

    import socket
    import time

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 0))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while True:
        msg = f'{time.time()}\n'.encode()
        sock.sendto(msg, ('<broadcast>', 5566))
        time.sleep(5)

Output:

.. code-block:: console

    $ nc -k -w 1 -ul 5566
    1431473025.72

Unix Domain Socket
------------------

Unix domain sockets provide inter-process communication on the same machine,
faster than TCP/IP loopback as they bypass the network stack.

.. code-block:: python

    import socket
    import contextlib
    import os

    @contextlib.contextmanager
    def domain_server(addr):
        try:
            if os.path.exists(addr):
                os.unlink(addr)
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.bind(addr)
            sock.listen(10)
            yield sock
        finally:
            sock.close()
            if os.path.exists(addr):
                os.unlink(addr)

    addr = "./domain.sock"
    with domain_server(addr) as sock:
        while True:
            conn, _ = sock.accept()
            msg = conn.recv(1024)
            conn.send(msg)
            conn.close()

Output:

.. code-block:: console

    $ nc -U ./domain.sock
    Hello
    Hello

Socket Pair for IPC
-------------------

``socketpair()`` creates a pair of connected sockets, useful for bidirectional
communication between parent and child processes.

.. code-block:: python

    import os
    import socket

    child_sock, parent_sock = socket.socketpair()
    pid = os.fork()

    try:
        if pid == 0:
            # Child process
            parent_sock.close()
            child_sock.send(b'Hello Parent!')
            msg = child_sock.recv(1024)
            print(f'Parent says: {msg}')
        else:
            # Parent process
            child_sock.close()
            msg = parent_sock.recv(1024)
            print(f'Child says: {msg}')
            parent_sock.send(b'Hello Child!')
            os.wait()
    finally:
        child_sock.close()
        parent_sock.close()

Output:

.. code-block:: bash

    $ python socketpair_demo.py
    Child says: b'Hello Parent!'
    Parent says: b'Hello Child!'

Threaded TCP Server
-------------------

Handle multiple clients concurrently using threads.

.. code-block:: python

    from threading import Thread
    import socket

    def handle_client(conn):
        while True:
            msg = conn.recv(1024)
            if not msg:
                break
            conn.send(msg)
        conn.close()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 5566))
    sock.listen(5)

    while True:
        conn, addr = sock.accept()
        t = Thread(target=handle_client, args=(conn,))
        t.daemon = True
        t.start()

Using sendfile for Zero-Copy Transfer
-------------------------------------

``os.sendfile()`` efficiently transfers file data to a socket without copying
through user space (zero-copy).

.. code-block:: python

    import os
    import socket
    import contextlib

    @contextlib.contextmanager
    def server(host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(10)
        try:
            yield s
        finally:
            s.close()

    def send_file(conn, filepath):
        with open(filepath, 'rb') as f:
            fd = f.fileno()
            size = os.fstat(fd).st_size
            offset = 0
            while size > 0:
                sent = os.sendfile(conn.fileno(), fd, offset, min(size, 65536))
                offset += sent
                size -= sent

    # Server that sends a file to each client
    with server('localhost', 5566) as s:
        while True:
            conn, addr = s.accept()
            send_file(conn, 'large_file.bin')
            conn.close()
