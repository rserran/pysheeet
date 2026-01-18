.. meta::
    :description lang=en: Python socket programming tutorial with examples for DNS resolution, TCP/UDP clients, IP address conversion, network byte order, timeouts, multicast, and SOCKS proxy
    :keywords: Python, socket, networking, TCP, UDP, DNS, IP address, hostname, getaddrinfo, inet_aton, inet_ntoa, network programming, timeout, multicast, SOCKS proxy, HTTP client

==============
Socket Basics
==============

.. contents:: Table of Contents
    :backlinks: none

Socket programming is the foundation of network communication in Python and virtually
all networked applications. A socket is an endpoint for sending and receiving data
across a network, providing a bidirectional communication channel between processes
on the same machine or across different machines over the Internet. While Python
provides high-level networking interfaces like ``urllib``, ``requests``, and ``asyncio``,
understanding low-level socket operations is essential for building custom protocols,
debugging network issues, implementing network tools, and interfacing with system-level
networking APIs.

This cheat sheet covers the fundamentals of socket programming in Python, including
hostname and DNS resolution, IP address manipulation, network byte order conversion,
timeout handling, multicast communication, and proxy support. Whether you're building
a simple client-server application, implementing a custom protocol, or troubleshooting
network connectivity issues, these examples provide the building blocks you need.

Get Hostname
------------

The ``socket.gethostname()`` function returns the current machine's hostname as
configured in the operating system, while ``socket.gethostbyname()`` performs a
DNS lookup to resolve a hostname to its IPv4 address. These functions are the most
basic building blocks for network programming, allowing your application to identify
itself and resolve other hosts on the network. Note that ``gethostbyname()`` only
returns IPv4 addresses; use ``getaddrinfo()`` for IPv6 support.

.. code-block:: python

    >>> import socket
    >>> socket.gethostname()
    'MacBookPro-4380.local'
    >>> hostname = socket.gethostname()
    >>> socket.gethostbyname(hostname)
    '172.20.10.4'
    >>> socket.gethostbyname('localhost')
    '127.0.0.1'

Get Address Info (DNS Resolution)
---------------------------------

``socket.getaddrinfo()`` is the most versatile and recommended function for DNS
resolution in modern Python code. Unlike ``gethostbyname()``, it supports both IPv4
and IPv6 addresses, returns multiple results when available, and provides complete
information including address family, socket type, protocol, canonical name, and
socket address. This function is essential for writing protocol-agnostic code that
works seamlessly with both IPv4 and IPv6 networks.

.. code-block:: python

    import socket
    import sys

    try:
        for res in socket.getaddrinfo(sys.argv[1], None,
                                      proto=socket.IPPROTO_TCP):
            family = res[0]
            sockaddr = res[4]
            print(family, sockaddr)
    except socket.gaierror:
        print("Invalid")

Output:

.. code-block:: console

    $ python gai.py 192.0.2.244
    AddressFamily.AF_INET ('192.0.2.244', 0)
    $ python gai.py 2001:db8:f00d::1:d
    AddressFamily.AF_INET6 ('2001:db8:f00d::1:d', 0, 0, 0)
    $ python gai.py www.google.com
    AddressFamily.AF_INET6 ('2607:f8b0:4006:818::2004', 0, 0, 0)
    AddressFamily.AF_INET ('172.217.10.132', 0)

It handles unusual cases, valid and invalid:

.. code-block:: console

    $ python gai.py 10.0.0.256  # octet overflow
    Invalid
    $ python gai.py not-exist.example.com  # unresolvable
    Invalid
    $ python gai.py fe80::1%eth0  # scoped
    AddressFamily.AF_INET6 ('fe80::1%eth0', 0, 0, 2)
    $ python gai.py ::ffff:192.0.2.128  # IPv4-Mapped
    AddressFamily.AF_INET6 ('::ffff:192.0.2.128', 0, 0, 0)
    $ python gai.py 0xc000027b  # IPv4 in hex
    AddressFamily.AF_INET ('192.0.2.123', 0)

Advanced DNS Queries
--------------------

While ``socket.getaddrinfo()`` handles basic hostname resolution, many applications
require more advanced DNS operations like querying specific record types. MX records
identify mail servers for a domain, TXT records store SPF and DKIM data for email
authentication, NS records list authoritative name servers, and SRV records enable
service discovery. The ``dnspython`` library provides a comprehensive DNS toolkit
that supports all record types, custom nameservers, DNSSEC validation, and zone
transfers. This is essential for building email validation systems, service discovery
mechanisms, and DNS monitoring tools.

.. code-block:: python

    # pip install dnspython
    import dns.resolver

    # Query MX records (mail servers)
    answers = dns.resolver.resolve('google.com', 'MX')
    for rdata in answers:
        print(f"MX: {rdata.exchange} (priority: {rdata.preference})")

    # Query TXT records (SPF, DKIM, etc.)
    answers = dns.resolver.resolve('google.com', 'TXT')
    for rdata in answers:
        print(f"TXT: {rdata}")

    # Query NS records (name servers)
    answers = dns.resolver.resolve('google.com', 'NS')
    for rdata in answers:
        print(f"NS: {rdata}")

    # Query A records with custom nameserver
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['8.8.8.8']  # Use Google DNS
    answers = resolver.resolve('example.com', 'A')
    for rdata in answers:
        print(f"A: {rdata}")

Reverse DNS Lookup
------------------

Reverse DNS (rDNS) lookup converts an IP address back to its associated hostname by
querying PTR records in the in-addr.arpa (IPv4) or ip6.arpa (IPv6) domains. This is
commonly used for logging to make IP addresses human-readable, security analysis to
verify that a connecting client's IP matches its claimed hostname, spam filtering
to check if mail servers have valid reverse DNS, and network troubleshooting to
identify devices on a network.

.. code-block:: python

    >>> import socket
    >>> # Reverse lookup returns (hostname, aliases, addresses)
    >>> socket.gethostbyaddr('8.8.8.8')
    ('dns.google', [], ['8.8.8.8'])
    >>> socket.gethostbyaddr('140.82.112.4')
    ('github.com', [], ['140.82.112.4'])

    >>> # Using getfqdn for fully qualified domain name
    >>> socket.getfqdn('8.8.8.8')
    'dns.google'

Network Byte Order Conversion
-----------------------------

Network protocols universally use big-endian byte order (most significant byte first),
also called "network byte order," while most modern CPUs (x86, ARM in little-endian
mode) use little-endian (least significant byte first). When sending multi-byte
integers over the network, you must convert from host byte order to network byte
order, and vice versa when receiving. The ``htons``/``htonl`` functions convert host
to network order for short (16-bit) and long (32-bit) integers, while ``ntohs``/``ntohl``
convert network to host order. Failing to perform these conversions causes subtle
bugs where values appear corrupted on machines with different endianness.

.. code-block:: python

    # little-endian machine
    >>> import socket
    >>> a = 1  # host endian
    >>> socket.htons(a)  # host to network short (16-bit)
    256
    >>> socket.htonl(a)  # host to network long (32-bit)
    16777216
    >>> socket.ntohs(256)  # network to host short
    1
    >>> socket.ntohl(16777216)  # network to host long
    1

IP Address String/Binary Conversion
-----------------------------------

IP addresses are typically displayed as human-readable strings (dotted-quad for IPv4
like "192.168.1.1", or colon-hex for IPv6 like "2001:db8::1"), but network protocols
transmit them as binary data (4 bytes for IPv4, 16 bytes for IPv6). The ``inet_aton``
and ``inet_ntoa`` functions convert between string and binary formats for IPv4 only.
For code that needs to support both IPv4 and IPv6, use ``inet_pton`` (presentation
to network) and ``inet_ntop`` (network to presentation), which take an address family
parameter to specify the IP version.

.. code-block:: python

    >>> import socket
    >>> # IPv4: string to binary
    >>> addr = socket.inet_aton('127.0.0.1')
    >>> addr
    b'\x7f\x00\x00\x01'
    >>> # IPv4: binary to string
    >>> socket.inet_ntoa(addr)
    '127.0.0.1'

    >>> # IPv4/IPv6: use inet_pton/inet_ntop
    >>> socket.inet_pton(socket.AF_INET, '192.168.1.1')
    b'\xc0\xa8\x01\x01'
    >>> socket.inet_pton(socket.AF_INET6, '::1')
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
    >>> socket.inet_ntop(socket.AF_INET6, b'\x00' * 15 + b'\x01')
    '::1'

MAC Address Conversion
----------------------

MAC (Media Access Control) addresses are 48-bit hardware identifiers assigned to
network interface cards, typically displayed as six colon-separated hexadecimal
pairs like "00:11:22:33:44:55". When working with raw Ethernet frames or ARP packets,
you need to convert between this human-readable format and the 6-byte binary format
used in network protocols. The ``binascii`` module provides ``hexlify`` and ``unhexlify``
functions for this conversion.

.. code-block:: python

    >>> import binascii
    >>> mac = '00:11:32:3c:c3:0b'
    >>> byte = binascii.unhexlify(mac.replace(':', ''))
    >>> byte
    b'\x00\x112<\xc3\x0b'
    >>> binascii.hexlify(byte)
    b'0011323cc30b'
    >>> # Format back to colon-separated
    >>> ':'.join(f'{b:02x}' for b in byte)
    '00:11:32:3c:c3:0b'

Check Port Availability
-----------------------

Before starting a server, you often need to verify that the desired port is available
for binding. Similarly, network monitoring tools need to check if remote services are
reachable. The ``is_port_open`` function attempts a TCP connection to test remote
service availability, while ``is_port_available`` tries to bind locally to check if
a port is free. These checks are essential for service health monitoring, port
scanning, and avoiding "Address already in use" errors when starting servers.

.. code-block:: python

    import socket

    def is_port_open(host, port, timeout=3):
        """Check if a port is open on a remote host."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            sock.connect((host, port))
            return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False
        finally:
            sock.close()

    def is_port_available(port):
        """Check if a local port is available for binding."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('', port))
            return True
        except OSError:
            return False
        finally:
            sock.close()

    # Usage
    print(is_port_open('google.com', 443))  # True
    print(is_port_available(8080))  # True if not in use

Get Network Interfaces
----------------------

Multi-homed servers (machines with multiple network interfaces) need to discover
their available IP addresses to bind to specific interfaces or advertise their
addresses to clients. The basic approach uses ``getaddrinfo`` on the hostname, but
for detailed interface information including interface names, netmasks, and broadcast
addresses, the ``netifaces`` library provides a cross-platform solution. This is
useful for network configuration tools, service discovery, and building applications
that need to select specific network interfaces.

.. code-block:: python

    import socket

    def get_local_ips():
        """Get all local IP addresses."""
        ips = []
        hostname = socket.gethostname()
        try:
            # Get all addresses for hostname
            for info in socket.getaddrinfo(hostname, None):
                ip = info[4][0]
                if ip not in ips:
                    ips.append(ip)
        except socket.gaierror:
            pass
        return ips

    # For more detailed interface info, use netifaces
    # pip install netifaces
    import netifaces

    for iface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in addrs:
            for addr in addrs[netifaces.AF_INET]:
                print(f"{iface}: {addr['addr']}")

Socket Options
--------------

Socket options control low-level socket behavior and are essential for building
robust network applications. ``SO_REUSEADDR`` allows immediate restart of servers
without waiting for TIME_WAIT to expire. ``SO_REUSEPORT`` enables multiple processes
to bind to the same port for load balancing. Buffer size options (``SO_SNDBUF``,
``SO_RCVBUF``) tune throughput for high-bandwidth applications. ``SO_KEEPALIVE``
detects dead connections by sending periodic probes. Understanding these options
helps you optimize performance and handle edge cases in production systems.

.. code-block:: python

    import socket

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Reuse address (avoid "Address already in use" error)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Reuse port (multiple processes can bind to same port)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    # Set send/receive buffer sizes
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)

    # Enable TCP keepalive
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

    # Set timeout (seconds)
    sock.settimeout(10.0)

    # Non-blocking mode
    sock.setblocking(False)

    # Get current option value
    print(sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF))

Troubleshooting: Connection Refused
-----------------------------------

"Connection refused" is one of the most common network errors, but its cause isn't
always obvious. It can mean the target port has no listening service, a firewall is
actively rejecting connections, or the service crashed. Other errors like "Connection
timed out" suggest the host is unreachable or a firewall is silently dropping packets,
while "Network unreachable" indicates routing problems. This diagnostic function
categorizes different error types to help identify the root cause, which is essential
for debugging network connectivity issues in development and production environments.

.. code-block:: python

    import socket
    import errno

    def diagnose_connection(host, port):
        """Diagnose connection issues."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        try:
            sock.connect((host, port))
            print(f"✓ Connected to {host}:{port}")
        except socket.timeout:
            print(f"✗ Timeout - host may be unreachable or firewalled")
        except ConnectionRefusedError:
            print(f"✗ Connection refused - no service on {port}")
        except socket.gaierror as e:
            print(f"✗ DNS error - cannot resolve {host}: {e}")
        except OSError as e:
            if e.errno == errno.ENETUNREACH:
                print(f"✗ Network unreachable")
            elif e.errno == errno.EHOSTUNREACH:
                print(f"✗ Host unreachable")
            else:
                print(f"✗ OS error: {e}")
        finally:
            sock.close()

    diagnose_connection('localhost', 8080)


Timeout Handling
----------------

Network operations can block indefinitely if a remote host becomes unresponsive,
a network path fails, or packets are lost. Without proper timeout handling, your
application may hang forever waiting for data that will never arrive. Python sockets
support timeouts at multiple levels: a global timeout via ``settimeout()`` that applies
to all operations, or per-operation timeouts using ``select()`` for more precise control.
Always set appropriate timeouts based on your application's requirements—too short
causes false failures, too long delays error detection.

.. code-block:: python

    import socket
    import errno

    def connect_with_timeout(host, port, timeout=5):
        """Connect with timeout and proper error handling."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            sock.connect((host, port))
            return sock
        except socket.timeout:
            print(f"Connection to {host}:{port} timed out")
            sock.close()
            return None
        except OSError as e:
            print(f"Connection failed: {e}")
            sock.close()
            return None

    def recv_with_timeout(sock, bufsize=4096, timeout=10):
        """Receive data with timeout."""
        sock.settimeout(timeout)
        try:
            return sock.recv(bufsize)
        except socket.timeout:
            return None  # Timeout, no data

    # Per-operation timeout using select
    import select

    def recv_timeout(sock, bufsize, timeout):
        """Receive with timeout using select (more precise)."""
        ready, _, _ = select.select([sock], [], [], timeout)
        if ready:
            return sock.recv(bufsize)
        raise socket.timeout("recv timed out")

Graceful Shutdown
-----------------

Simply calling ``close()`` on a socket may lose data still in transit. The TCP
protocol requires a proper four-way handshake (FIN-ACK sequence) to ensure both
sides have finished sending. The ``shutdown()`` method provides fine-grained control:
``SHUT_WR`` sends a FIN packet signaling "I'm done sending" while still allowing
reads, ``SHUT_RD`` stops receiving, and ``SHUT_RDWR`` does both. For clean termination,
call ``shutdown(SHUT_WR)`` first, drain any remaining incoming data, then ``close()``.
This pattern is especially important for protocols where the server waits for client
EOF before sending its final response.

.. code-block:: python

    import socket

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('example.com', 80))
    sock.send(b'GET / HTTP/1.0\r\nHost: example.com\r\n\r\n')

    # Shutdown write side - signals EOF to server
    sock.shutdown(socket.SHUT_WR)

    # Read remaining data
    response = b''
    while True:
        data = sock.recv(4096)
        if not data:
            break
        response += data

    # Now close the socket
    sock.close()

    # shutdown options:
    # SHUT_RD   - no more reads
    # SHUT_WR   - no more writes (sends FIN)
    # SHUT_RDWR - no more reads or writes

Multicast UDP
-------------

Multicast is a one-to-many communication model where a single packet is delivered
to multiple receivers simultaneously. Unlike broadcast (which floods the entire
network) or unicast (one sender, one receiver), multicast uses special IP addresses
(224.0.0.0 to 239.255.255.255) and IGMP protocol to efficiently route packets only
to interested receivers. Receivers must explicitly join a multicast group to receive
traffic. The TTL (Time To Live) controls how far packets travel—TTL=1 stays on the
local subnet, higher values cross routers. Multicast is ideal for streaming media,
real-time data feeds, and service discovery where the same data goes to many clients.

.. code-block:: python

    import socket
    import struct

    MCAST_GROUP = '224.1.1.1'
    MCAST_PORT = 5007

    # Sender
    def multicast_sender():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.sendto(b'Hello Multicast!', (MCAST_GROUP, MCAST_PORT))
        sock.close()

    # Receiver
    def multicast_receiver():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', MCAST_PORT))

        # Join multicast group
        mreq = struct.pack('4sl', socket.inet_aton(MCAST_GROUP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        data, addr = sock.recvfrom(1024)
        print(f"Received: {data} from {addr}")
        sock.close()

HTTP Client with Sockets
------------------------

While high-level libraries like ``urllib`` and ``requests`` handle HTTP elegantly,
understanding raw HTTP over sockets is invaluable for debugging, implementing custom
protocols, or working in constrained environments. HTTP/1.1 is a text-based protocol:
you send a request line (``GET /path HTTP/1.1``), headers (key-value pairs), a blank
line, and optionally a body. The server responds similarly. Key headers include
``Host`` (required in HTTP/1.1), ``Connection: close`` (to signal single request),
and ``Content-Length`` for bodies. This low-level approach reveals exactly what's
happening on the wire, making it easier to diagnose issues like malformed headers,
encoding problems, or TLS handshake failures.

.. code-block:: python

    import socket
    import ssl

    def http_get(host, path='/', port=80, use_ssl=False):
        """Simple HTTP GET using raw sockets."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if use_ssl:
            context = ssl.create_default_context()
            sock = context.wrap_socket(sock, server_hostname=host)
            port = 443

        sock.connect((host, port))

        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        sock.send(request.encode())

        response = b''
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data

        sock.close()

        # Split headers and body
        header_end = response.find(b'\r\n\r\n')
        headers = response[:header_end].decode()
        body = response[header_end + 4:]

        return headers, body

    # Usage
    headers, body = http_get('example.com', '/', use_ssl=True)
    print(headers)

SOCKS Proxy Support
-------------------

SOCKS (Socket Secure) is a protocol that routes network traffic through a proxy
server, providing anonymity and the ability to bypass firewalls or geographic
restrictions. Unlike HTTP proxies that only handle HTTP traffic, SOCKS operates
at a lower level and can proxy any TCP (and with SOCKS5, UDP) traffic. SOCKS5
adds authentication and IPv6 support. Common use cases include routing traffic
through Tor (which uses SOCKS5 on port 9050), accessing internal networks via
SSH tunnels (``ssh -D``), or corporate proxy requirements. The ``PySocks`` library
makes it easy to route Python socket connections through SOCKS proxies, either
globally (patching all sockets) or per-connection.

.. code-block:: python

    # pip install PySocks
    import socks
    import socket

    # Method 1: Patch all sockets globally
    socks.set_default_proxy(socks.SOCKS5, "localhost", 9050)
    socket.socket = socks.socksocket

    # Now all socket connections go through the proxy
    s = socket.socket()
    s.connect(("example.com", 80))

    # Method 2: Create proxy socket directly
    s = socks.socksocket()
    s.set_proxy(socks.SOCKS5, "localhost", 9050)
    s.connect(("example.com", 80))

    # Method 3: With authentication
    s = socks.socksocket()
    s.set_proxy(socks.SOCKS5, "proxy.example.com", 1080,
                username="user", password="pass")
