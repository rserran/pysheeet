.. meta::
    :description lang=en: Python TLS/SSL socket programming tutorial covering secure servers, certificate handling, cipher configuration, mutual TLS (mTLS), and non-blocking SSL for HTTPS and encrypted communication
    :keywords: Python, socket, SSL, TLS, secure socket, certificate, cipher, HTTPS, encryption, network security, mTLS, mutual TLS, X.509, OpenSSL, cryptography

==================
SSL/TLS Sockets
==================

.. contents:: Table of Contents
    :backlinks: none

Transport Layer Security (TLS), formerly known as Secure Sockets Layer (SSL), is the
standard protocol for encrypting network communication. TLS provides three essential
security properties: confidentiality (data is encrypted and cannot be read by
eavesdroppers), integrity (data cannot be modified in transit without detection),
and authentication (parties can verify each other's identity using certificates).
Every HTTPS connection, secure email, and VPN uses TLS under the hood.

Python's ``ssl`` module provides a comprehensive interface for TLS, allowing you to
wrap regular sockets with encryption. This section covers creating TLS-enabled servers
and clients, configuring cipher suites for security compliance, handling X.509
certificates, implementing mutual TLS (mTLS) for client authentication, and building
non-blocking TLS servers for high-performance applications. Whether you're building
a secure API server, implementing certificate pinning, or debugging TLS handshake
issues, these examples provide the foundation you need.

Simple TLS Echo Server
----------------------

A basic TLS server wraps accepted TCP connections with an SSL context to provide
encryption. The server requires a certificate (public key) and private key, which
can be self-signed for testing or obtained from a Certificate Authority (CA) for
production use. The ``SSLContext`` object manages all TLS settings including protocol
version, cipher suites, and certificate verification options.

.. code-block:: python

    import socket
    import ssl

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 5566))
    sock.listen(10)

    sslctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    sslctx.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

    try:
        while True:
            conn, addr = sock.accept()
            sslconn = sslctx.wrap_socket(conn, server_side=True)
            msg = sslconn.recv(1024)
            if msg:
                sslconn.send(msg)
            sslconn.close()
    finally:
        sock.close()

Generate self-signed certificate and test:

.. code-block:: bash

    # Generate private key and self-signed certificate
    $ openssl genrsa -out key.pem 2048
    $ openssl req -x509 -new -nodes -key key.pem -days 365 -out cert.pem

    # Run server
    $ python3 ssl_server.py &

    # Test with openssl client
    $ openssl s_client -connect localhost:5566
    Hello SSL
    Hello SSL

TLS Server with Cipher Configuration
------------------------------------

Configure specific cipher suites for security compliance or compatibility.

.. code-block:: python

    import socket
    import ssl
    import json

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 5566))
    sock.listen(10)

    sslctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    sslctx.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

    # Set specific ciphers (TLS 1.2)
    sslctx.set_ciphers('ECDHE+AESGCM:DHE+AESGCM')

    # Print configured ciphers
    print(json.dumps(sslctx.get_ciphers(), indent=2))

    try:
        while True:
            conn, addr = sock.accept()
            sslconn = sslctx.wrap_socket(conn, server_side=True)
            print(f"Cipher: {sslconn.cipher()}")
            msg = sslconn.recv(1024)
            if msg:
                sslconn.send(msg)
            sslconn.close()
    finally:
        sock.close()

TLS Client
----------

Connect to a TLS server with certificate verification.

.. code-block:: python

    import socket
    import ssl

    hostname = 'www.google.com'
    port = 443

    # Create default SSL context (verifies certificates)
    context = ssl.create_default_context()

    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            print(f"TLS version: {ssock.version()}")
            print(f"Cipher: {ssock.cipher()}")

            # Send HTTP request
            ssock.send(b"GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n")
            response = ssock.recv(4096)
            print(response[:200])

TLS Client with Custom CA
-------------------------

Verify server certificate against a custom Certificate Authority.

.. code-block:: python

    import socket
    import ssl

    hostname = 'localhost'
    port = 5566

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations('ca-cert.pem')  # CA certificate
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED

    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            ssock.send(b"Hello")
            print(ssock.recv(1024))

Mutual TLS (mTLS)
-----------------

Both client and server present certificates for mutual authentication.

Server:

.. code-block:: python

    import socket
    import ssl

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 5566))
    sock.listen(10)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('server-cert.pem', 'server-key.pem')
    context.load_verify_locations('ca-cert.pem')
    context.verify_mode = ssl.CERT_REQUIRED  # Require client cert

    try:
        while True:
            conn, addr = sock.accept()
            sslconn = context.wrap_socket(conn, server_side=True)
            # Get client certificate info
            cert = sslconn.getpeercert()
            print(f"Client: {cert.get('subject')}")
            msg = sslconn.recv(1024)
            if msg:
                sslconn.send(msg)
            sslconn.close()
    finally:
        sock.close()

Client:

.. code-block:: python

    import socket
    import ssl

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_cert_chain('client-cert.pem', 'client-key.pem')
    context.load_verify_locations('ca-cert.pem')

    with socket.create_connection(('localhost', 5566)) as sock:
        with context.wrap_socket(sock, server_hostname='localhost') as ssock:
            ssock.send(b"Hello mTLS")
            print(ssock.recv(1024))

Non-blocking TLS with selectors
-------------------------------

Handle TLS handshake and I/O asynchronously using the selectors module.

.. code-block:: python

    import socket
    import selectors
    import ssl
    from functools import partial

    sslctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    sslctx.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    def accept(sock, sel):
        conn, addr = sock.accept()
        sslconn = sslctx.wrap_socket(conn,
                                     server_side=True,
                                     do_handshake_on_connect=False)
        sel.register(sslconn, selectors.EVENT_READ, do_handshake)

    def do_handshake(sslconn, sel):
        try:
            sslconn.do_handshake()
            sel.modify(sslconn, selectors.EVENT_READ, read)
        except ssl.SSLWantReadError:
            pass  # Need more data, wait for next event
        except ssl.SSLWantWriteError:
            sel.modify(sslconn, selectors.EVENT_WRITE, do_handshake)

    def read(sslconn, sel):
        try:
            msg = sslconn.recv(1024)
            if msg:
                sel.modify(sslconn, selectors.EVENT_WRITE,
                          partial(write, msg=msg))
            else:
                sel.unregister(sslconn)
                sslconn.close()
        except ssl.SSLWantReadError:
            pass

    def write(sslconn, sel, msg=None):
        try:
            if msg:
                sslconn.send(msg)
            sel.modify(sslconn, selectors.EVENT_READ, read)
        except ssl.SSLWantWriteError:
            pass

    # Main server loop
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 5566))
    sock.listen(10)

    sel = selectors.DefaultSelector()
    sel.register(sock, selectors.EVENT_READ, accept)

    try:
        while True:
            events = sel.select()
            for key, mask in events:
                handler = key.data
                handler(key.fileobj, sel)
    except KeyboardInterrupt:
        pass
    finally:
        sock.close()
        sel.close()

Get Certificate Information
---------------------------

Retrieve and inspect server certificate details.

.. code-block:: python

    import socket
    import ssl
    import pprint

    hostname = 'www.google.com'
    port = 443

    context = ssl.create_default_context()

    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            pprint.pprint(cert)

            # Get specific fields
            print(f"Subject: {dict(x[0] for x in cert['subject'])}")
            print(f"Issuer: {dict(x[0] for x in cert['issuer'])}")
            print(f"Not Before: {cert['notBefore']}")
            print(f"Not After: {cert['notAfter']}")

            # Get certificate in DER format
            der_cert = ssock.getpeercert(binary_form=True)
            print(f"Certificate size: {len(der_cert)} bytes")

TLS Version and Security Settings
---------------------------------

Configure minimum TLS version and security options.

.. code-block:: python

    import ssl

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    # Set minimum TLS version (TLS 1.2+)
    context.minimum_version = ssl.TLSVersion.TLSv1_2

    # Disable older protocols explicitly
    context.options |= ssl.OP_NO_SSLv2
    context.options |= ssl.OP_NO_SSLv3
    context.options |= ssl.OP_NO_TLSv1
    context.options |= ssl.OP_NO_TLSv1_1

    # Disable compression (CRIME attack mitigation)
    context.options |= ssl.OP_NO_COMPRESSION

    # Use server's cipher preference
    context.options |= ssl.OP_CIPHER_SERVER_PREFERENCE

    # Load certificate
    context.load_cert_chain('cert.pem', 'key.pem')

    # Set strong ciphers only
    context.set_ciphers('ECDHE+AESGCM:DHE+AESGCM:!aNULL:!MD5:!DSS')

    print(f"Min version: {context.minimum_version}")
    print(f"Ciphers: {len(context.get_ciphers())}")
