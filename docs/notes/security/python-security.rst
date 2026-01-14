.. meta::
    :description lang=en: Legacy Python security examples using older libraries (PyCrypto, pyOpenSSL) for reference and compatibility
    :keywords: Python, Python3, Security, PyCrypto, pyOpenSSL, Legacy, Deprecated

=============================
Security (Legacy Examples)
=============================

.. contents:: Table of Contents
    :backlinks: none

.. warning::

    This page contains **legacy examples** using older libraries like PyCrypto
    and pyOpenSSL. For new projects, use the modern ``cryptography`` library
    instead. See the :doc:`../cryptography/python-crypto` guide for secure,
    up-to-date examples.

    **Key issues with examples on this page:**

    - PyCrypto is unmaintained (use ``cryptography`` or ``PyCryptodome``)
    - Some examples use weak algorithms (SHA1, small key sizes)
    - AES-CBC without authentication is vulnerable to padding oracle attacks
    - PKCS#1 v1.5 padding is vulnerable (use OAEP instead)
    - ``ssl.wrap_socket`` is deprecated (use ``SSLContext``)

    These examples are preserved for reference when working with legacy systems.

Legacy: Simple HTTPS Server
---------------------------

.. note::

    For modern HTTPS servers, see :doc:`../cryptography/python-tls`.

This example uses the deprecated ``ssl.wrap_socket``. Modern code should use
``SSLContext`` instead.

.. code-block:: python

    # Legacy Python 3 example (deprecated pattern)
    from http import server
    import ssl

    host, port = 'localhost', 5566
    handler = server.SimpleHTTPRequestHandler
    httpd = server.HTTPServer((host, port), handler)

    # DEPRECATED: Use SSLContext instead
    httpd.socket = ssl.wrap_socket(
        httpd.socket,
        certfile='./cert.crt',
        keyfile='./cert.key',
        server_side=True
    )
    httpd.serve_forever()

Legacy: RSA with PyCrypto
-------------------------

.. note::

    For modern RSA encryption, see :doc:`../cryptography/python-crypto`.
    Use RSA-OAEP padding, not PKCS#1 v1.5.

These examples use PyCrypto which is unmaintained. Use ``cryptography`` library
for new projects.

.. code-block:: python

    # LEGACY: Using PyCrypto (unmaintained)
    # For new code, use cryptography library with OAEP padding

    from Crypto.PublicKey import RSA
    from Crypto.Cipher import PKCS1_v1_5  # INSECURE: Use OAEP instead
    import base64

    # Encrypt (INSECURE PATTERN)
    with open('public.key', 'rb') as f:
        pubkey = RSA.importKey(f.read())

    cipher = PKCS1_v1_5.new(pubkey)
    ciphertext = cipher.encrypt(b"Hello RSA!")
    print(base64.b64encode(ciphertext).decode())

Legacy: AES-CBC with PyCrypto
-----------------------------

.. note::

    AES-CBC without authentication is vulnerable to padding oracle attacks.
    For modern encryption, use AES-GCM which provides authenticated encryption.
    See :doc:`../cryptography/python-crypto`.

.. code-block:: python

    # LEGACY: AES-CBC without authentication (INSECURE)
    # For new code, use AES-GCM from cryptography library

    from Crypto.Cipher import AES
    from Crypto.Random.random import getrandbits
    import struct

    BS = 16
    pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode()
    unpad = lambda s: s[:-s[-1]]

    key = struct.pack('=QQ', getrandbits(64), getrandbits(64))
    iv = struct.pack('=QQ', getrandbits(64), getrandbits(64))

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(b"Secret message"))

    # PROBLEM: No authentication - attacker can modify ciphertext

Legacy: Digital Signatures with PyCrypto
----------------------------------------

.. note::

    For modern signatures, use Ed25519 or RSA-PSS from the ``cryptography``
    library. See :doc:`../cryptography/python-crypto`.

.. code-block:: python

    # LEGACY: Using PyCrypto with SHA256
    from Crypto.PublicKey import RSA
    from Crypto.Signature import PKCS1_v1_5  # Consider PSS for new code
    from Crypto.Hash import SHA256

    def sign(privkey, data):
        rsakey = RSA.importKey(privkey)
        signer = PKCS1_v1_5.new(rsakey)
        digest = SHA256.new()
        digest.update(data)
        return signer.sign(digest)

    def verify(pubkey, sig, data):
        rsakey = RSA.importKey(pubkey)
        verifier = PKCS1_v1_5.new(rsakey)
        digest = SHA256.new()
        digest.update(data)
        return verifier.verify(digest, sig)

Legacy: Certificate Generation with pyOpenSSL
---------------------------------------------

.. note::

    For modern certificate generation, use the ``cryptography`` library directly.
    See :doc:`../cryptography/python-tls`.

.. code-block:: python

    # LEGACY: Using pyOpenSSL
    # For new code, use cryptography library directly

    from datetime import datetime, timedelta
    from OpenSSL import crypto

    # Load private key
    with open('key.pem', 'rb') as f:
        key = crypto.load_privatekey(crypto.FILETYPE_PEM, f.read())

    now = datetime.now()
    expire = now + timedelta(days=365)

    cert = crypto.X509()
    cert.get_subject().C = "US"
    cert.get_subject().ST = "California"
    cert.get_subject().L = "San Francisco"
    cert.get_subject().O = "Example Org"
    cert.get_subject().CN = "example.com"
    cert.set_serial_number(1000)
    cert.set_notBefore(now.strftime("%Y%m%d%H%M%SZ").encode())
    cert.set_notAfter(expire.strftime("%Y%m%d%H%M%SZ").encode())
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(key, 'sha256')  # Use SHA256, not SHA1

    with open('cert.pem', 'wb') as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

Migration Guide
---------------

If you have code using these legacy patterns, here's how to migrate:

**PyCrypto → cryptography library:**

.. code-block:: python

    # OLD (PyCrypto)
    from Crypto.Cipher import AES
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # NEW (cryptography) - Use authenticated encryption
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data)

**ssl.wrap_socket → SSLContext:**

.. code-block:: python

    # OLD
    ssl.wrap_socket(sock, certfile='cert.pem', keyfile='key.pem')

    # NEW
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')
    context.wrap_socket(sock, server_side=True)

**PKCS#1 v1.5 → OAEP:**

.. code-block:: python

    # OLD (insecure)
    from Crypto.Cipher import PKCS1_v1_5
    cipher = PKCS1_v1_5.new(key)

    # NEW (secure)
    from cryptography.hazmat.primitives.asymmetric import padding
    ciphertext = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
