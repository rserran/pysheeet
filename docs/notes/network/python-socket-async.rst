.. meta::
    :description lang=en: Python asynchronous socket programming tutorial with select, poll, epoll, kqueue, and selectors module for building high-performance non-blocking servers
    :keywords: Python, socket, async, select, poll, epoll, kqueue, selectors, non-blocking, event-driven, I/O multiplexing, concurrent connections, high-performance server

=================
Async Socket I/O
=================

.. contents:: Table of Contents
    :backlinks: none

Asynchronous I/O is essential for building high-performance network servers that can
handle thousands of concurrent connections efficiently. Traditional blocking I/O
requires one thread per connection, which doesn't scale well due to memory overhead
and context switching costs. Asynchronous I/O solves this by allowing a single thread
to handle multiple connections using I/O multiplexing—the program monitors multiple
sockets simultaneously and processes whichever ones are ready for reading or writing.

This section covers the evolution of I/O multiplexing in Python, from the classic
``select()`` system call (portable but limited) to modern high-performance mechanisms
like ``epoll`` (Linux) and ``kqueue`` (BSD/macOS) that can efficiently handle tens of
thousands of connections. We also cover the ``selectors`` module, which provides a
high-level, platform-independent interface that automatically uses the best available
mechanism. Understanding these primitives is valuable even if you use higher-level
frameworks like ``asyncio``, as they build upon these same concepts.

Async TCP Server - select
-------------------------

``select()`` is the oldest and most portable I/O multiplexing mechanism, available on
virtually all platforms including Windows, Linux, and macOS. It monitors file descriptors
for three conditions: readability (data available to read), writability (buffer space
available to write), and exceptional conditions (errors). While portable, ``select()``
has limitations: it typically supports only up to 1024 file descriptors and has O(n)
performance as it must scan all monitored descriptors on each call.

.. code-block:: python

    from select import select
    import socket

    host = ('localhost', 5566)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(host)
    sock.listen(5)

    read_list = [sock]
    write_list = []
    messages = {}

    try:
        while True:
            readable, writable, _ = select(read_list, write_list, [])

            for s in readable:
                if s == sock:
                    conn, addr = sock.accept()
                    read_list.append(conn)
                else:
                    msg = s.recv(1024)
                    if msg:
                        messages[s.fileno()] = msg
                        write_list.append(s)
                    else:
                        read_list.remove(s)
                        s.close()

            for s in writable:
                msg = messages.pop(s.fileno(), None)
                if msg:
                    s.send(msg)
                write_list.remove(s)
    except KeyboardInterrupt:
        sock.close()

Async TCP Server - poll
-----------------------

``poll()`` is similar to ``select()`` but more efficient for large numbers of
file descriptors. Available on Unix systems.

.. code-block:: python

    import socket
    import select
    import contextlib

    host = 'localhost'
    port = 5566

    connections = {}
    requests = {}
    responses = {}

    @contextlib.contextmanager
    def create_server(host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setblocking(False)
        s.bind((host, port))
        s.listen(10)
        try:
            yield s
        finally:
            s.close()

    def accept(server, poll):
        conn, addr = server.accept()
        conn.setblocking(False)
        fd = conn.fileno()
        poll.register(fd, select.POLLIN)
        requests[fd] = conn
        connections[fd] = conn

    def recv(fd, poll):
        conn = requests.pop(fd, None)
        if not conn:
            return
        msg = conn.recv(1024)
        if msg:
            responses[fd] = msg
            poll.modify(fd, select.POLLOUT)
        else:
            poll.unregister(fd)
            conn.close()
            connections.pop(fd, None)

    def send(fd, poll):
        conn = connections.get(fd)
        msg = responses.pop(fd, None)
        if conn and msg:
            conn.send(msg)
            requests[fd] = conn
            poll.modify(fd, select.POLLIN)

    with create_server(host, port) as server:
        poll = select.poll()
        poll.register(server.fileno(), select.POLLIN)

        try:
            while True:
                events = poll.poll(1000)
                for fd, event in events:
                    if fd == server.fileno():
                        accept(server, poll)
                    elif event & (select.POLLIN | select.POLLPRI):
                        recv(fd, poll)
                    elif event & select.POLLOUT:
                        send(fd, poll)
        except KeyboardInterrupt:
            pass

Async TCP Server - epoll
------------------------

``epoll`` is Linux-specific and the most efficient for handling thousands of
connections. It uses edge-triggered or level-triggered notifications.

.. code-block:: python

    import socket
    import select
    import contextlib

    host = 'localhost'
    port = 5566

    connections = {}
    requests = {}
    responses = {}

    @contextlib.contextmanager
    def create_server(host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setblocking(False)
        s.bind((host, port))
        s.listen(10)
        try:
            yield s
        finally:
            s.close()

    def accept(server, epoll):
        conn, addr = server.accept()
        conn.setblocking(False)
        fd = conn.fileno()
        epoll.register(fd, select.EPOLLIN)
        requests[fd] = conn
        connections[fd] = conn

    def recv(fd, epoll):
        conn = requests.pop(fd, None)
        if not conn:
            return
        msg = conn.recv(1024)
        if msg:
            responses[fd] = msg
            epoll.modify(fd, select.EPOLLOUT)
        else:
            epoll.unregister(fd)
            conn.close()
            connections.pop(fd, None)

    def send(fd, epoll):
        conn = connections.get(fd)
        msg = responses.pop(fd, None)
        if conn and msg:
            conn.send(msg)
            requests[fd] = conn
            epoll.modify(fd, select.EPOLLIN)

    with create_server(host, port) as server:
        epoll = select.epoll()
        epoll.register(server.fileno(), select.EPOLLIN)

        try:
            while True:
                events = epoll.poll(1)
                for fd, event in events:
                    if fd == server.fileno():
                        accept(server, epoll)
                    elif event & select.EPOLLIN:
                        recv(fd, epoll)
                    elif event & select.EPOLLOUT:
                        send(fd, epoll)
        except KeyboardInterrupt:
            pass
        finally:
            epoll.close()

Async TCP Server - kqueue
-------------------------

``kqueue`` is the BSD/macOS equivalent of epoll, providing efficient event
notification for large numbers of file descriptors.

.. code-block:: python

    import socket
    import select
    import contextlib

    if not hasattr(select, 'kqueue'):
        print("kqueue not supported on this platform")
        exit(1)

    host = 'localhost'
    port = 5566

    connections = {}
    requests = {}
    responses = {}

    @contextlib.contextmanager
    def create_server(host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setblocking(False)
        s.bind((host, port))
        s.listen(10)
        try:
            yield s
        finally:
            s.close()

    def accept(server, kq):
        conn, addr = server.accept()
        conn.setblocking(False)
        fd = conn.fileno()
        ke = select.kevent(fd, select.KQ_FILTER_READ, select.KQ_EV_ADD)
        kq.control([ke], 0)
        requests[fd] = conn
        connections[fd] = conn

    def recv(fd, kq):
        conn = requests.pop(fd, None)
        if not conn:
            return
        msg = conn.recv(1024)
        if msg:
            responses[fd] = msg
            # Switch from read to write
            ke_del = select.kevent(fd, select.KQ_FILTER_READ, select.KQ_EV_DELETE)
            ke_add = select.kevent(fd, select.KQ_FILTER_WRITE, select.KQ_EV_ADD)
            kq.control([ke_del, ke_add], 0)
            requests[fd] = conn
        else:
            ke = select.kevent(fd, select.KQ_FILTER_READ, select.KQ_EV_DELETE)
            kq.control([ke], 0)
            conn.close()
            connections.pop(fd, None)

    def send(fd, kq):
        conn = connections.get(fd)
        msg = responses.pop(fd, None)
        if conn and msg:
            conn.send(msg)
            # Switch from write to read
            ke_del = select.kevent(fd, select.KQ_FILTER_WRITE, select.KQ_EV_DELETE)
            ke_add = select.kevent(fd, select.KQ_FILTER_READ, select.KQ_EV_ADD)
            kq.control([ke_del, ke_add], 0)
            requests[fd] = conn

    with create_server(host, port) as server:
        kq = select.kqueue()
        ke = select.kevent(server.fileno(), select.KQ_FILTER_READ, select.KQ_EV_ADD)
        kq.control([ke], 0)

        try:
            while True:
                events = kq.control(None, 1024, 1)
                for e in events:
                    fd = e.ident
                    if fd == server.fileno():
                        accept(server, kq)
                    elif e.filter == select.KQ_FILTER_READ:
                        recv(fd, kq)
                    elif e.filter == select.KQ_FILTER_WRITE:
                        send(fd, kq)
        except KeyboardInterrupt:
            pass
        finally:
            kq.close()

High-Level API - selectors
--------------------------

The ``selectors`` module (Python 3.4+) provides a high-level, platform-independent
interface that automatically uses the best available mechanism (epoll, kqueue, etc.).

.. code-block:: python

    import selectors
    import socket
    import contextlib

    @contextlib.contextmanager
    def create_server(host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(10)
        sel = selectors.DefaultSelector()
        try:
            yield s, sel
        finally:
            s.close()
            sel.close()

    def accept_handler(sock, sel):
        conn, addr = sock.accept()
        sel.register(conn, selectors.EVENT_READ, read_handler)

    def read_handler(conn, sel):
        msg = conn.recv(1024)
        if msg:
            conn.send(msg)
        else:
            sel.unregister(conn)
            conn.close()

    host = 'localhost'
    port = 5566

    with create_server(host, port) as (sock, sel):
        sel.register(sock, selectors.EVENT_READ, accept_handler)
        try:
            while True:
                events = sel.select()
                for key, mask in events:
                    handler = key.data
                    handler(key.fileobj, sel)
        except KeyboardInterrupt:
            pass

Comparison of I/O Multiplexing Methods
--------------------------------------

+------------+------------+------------------+---------------------------+
| Method     | Platform   | Scalability      | Notes                     |
+============+============+==================+===========================+
| select     | All        | O(n) - Limited   | Max ~1024 FDs             |
+------------+------------+------------------+---------------------------+
| poll       | Unix       | O(n) - Better    | No FD limit               |
+------------+------------+------------------+---------------------------+
| epoll      | Linux      | O(1) - Excellent | Edge/level triggered      |
+------------+------------+------------------+---------------------------+
| kqueue     | BSD/macOS  | O(1) - Excellent | Similar to epoll          |
+------------+------------+------------------+---------------------------+
| selectors  | All        | Best available   | Recommended for new code  |
+------------+------------+------------------+---------------------------+

.. note::

    For new code, use the ``selectors`` module or ``asyncio`` for async I/O.
    The low-level APIs (select, poll, epoll, kqueue) are mainly useful for
    understanding how async I/O works or when you need fine-grained control.
