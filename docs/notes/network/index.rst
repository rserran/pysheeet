.. meta::
    :description lang=en: Python network programming tutorial covering sockets, TCP/UDP servers, async I/O, SSL/TLS, packet sniffing, and SSH tunneling
    :keywords: Python, Python3, socket, networking, TCP, UDP, SSL, TLS, async, select, epoll, SSH, packet sniffing, server, client

=======
Network
=======

Network programming is fundamental to modern software development, enabling
communication between processes across machines, data centers, and the internet.
This section covers Python's networking capabilities from low-level socket
programming to secure communications. You'll find practical examples for building
TCP/UDP servers, handling multiple connections with async I/O (select, poll, epoll),
implementing TLS/SSL encryption, packet sniffing for network analysis, and SSH
for secure remote access and tunneling. Whether you're building web services,
IoT applications, network tools, or automation scripts, these cheat sheets provide
the essential patterns and code snippets you need.

.. toctree::
    :maxdepth: 1

    python-socket
    python-socket-server
    python-socket-async
    python-socket-ssl
    python-socket-sniffer
    python-ssh
