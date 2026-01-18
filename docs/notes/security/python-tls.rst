.. meta::
    :description lang=en: Python TLS/SSL and X.509 certificate guide covering secure HTTPS servers, certificate generation, CSR creation, and certificate verification using the cryptography library
    :keywords: Python, Python3, TLS, SSL, HTTPS, X.509, Certificate, CSR, Certificate Authority, Self-Signed, SSLContext, cryptography

========================
TLS/SSL and Certificates
========================

.. contents:: Table of Contents
    :backlinks: none

Transport Layer Security (TLS) provides encrypted, authenticated communication
over networks. This guide covers creating secure HTTPS servers, generating
certificates, and proper TLS configuration in Python. We use the ``ssl`` module's
``SSLContext`` API (not the deprecated ``wrap_socket``) and the ``cryptography``
library for certificate operations. Always use TLS 1.2 or 1.3—older versions have
known vulnerabilities.

.. warning::

    For production, always use certificates from a trusted Certificate Authority
    (CA) like Let's Encrypt. Self-signed certificates are only for development
    and testing. Never disable certificate verification in production code.

Secure HTTPS Server
-------------------

Create an HTTPS server using ``SSLContext`` with secure defaults. The context
configures TLS version, cipher suites, and certificate verification. Always
load both the certificate chain and private key. For production, use certificates
from a real CA.

.. code-block:: python

    import ssl
    from http.server import HTTPServer, SimpleHTTPRequestHandler

    def create_secure_context(certfile, keyfile):
        """Create SSLContext with secure defaults."""
        # TLS 1.2+ only, secure ciphers
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.minimum_version = ssl.TLSVersion.TLSv1_2

        # Load certificate and private key
        context.load_cert_chain(certfile=certfile, keyfile=keyfile)

        # Disable insecure options
        context.options |= ssl.OP_NO_SSLv2
        context.options |= ssl.OP_NO_SSLv3
        context.options |= ssl.OP_NO_TLSv1
        context.options |= ssl.OP_NO_TLSv1_1

        return context

    # Create server
    host, port = "localhost", 8443
    context = create_secure_context("cert.pem", "key.pem")

    httpd = HTTPServer((host, port), SimpleHTTPRequestHandler)
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

    print(f"Serving HTTPS on https://{host}:{port}")
    httpd.serve_forever()

Secure HTTPS Client
-------------------

When making HTTPS requests, Python verifies certificates by default. For custom
CA certificates or client authentication, configure an ``SSLContext``. Never
set ``verify=False`` or disable hostname checking in production.

.. code-block:: python

    import ssl
    import urllib.request

    # Default secure context (verifies certificates)
    context = ssl.create_default_context()

    # Make HTTPS request
    url = "https://example.com"
    with urllib.request.urlopen(url, context=context) as response:
        print(response.read().decode())

    # Custom CA certificate (e.g., internal CA)
    context = ssl.create_default_context()
    context.load_verify_locations("internal-ca.pem")

    # Client certificate authentication (mTLS)
    context = ssl.create_default_context()
    context.load_cert_chain(certfile="client.pem", keyfile="client-key.pem")

    # Using requests library (recommended for HTTP)
    import requests

    # Default (secure)
    response = requests.get("https://example.com")

    # Custom CA
    response = requests.get("https://internal.example.com", verify="internal-ca.pem")

    # Client certificate
    response = requests.get(
        "https://secure.example.com",
        cert=("client.pem", "client-key.pem"),
    )

Generate Self-Signed Certificate
--------------------------------

Self-signed certificates are useful for development and testing. The certificate
is signed by its own private key rather than a CA. Browsers will show warnings
for self-signed certificates. Use the ``cryptography`` library for certificate
generation—it's more Pythonic than calling OpenSSL.

.. code-block:: python

    import ipaddress
    from datetime import datetime, timedelta
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization

    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )

    # Certificate subject and issuer (same for self-signed)
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "My Organization"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])

    # Build certificate
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=365))
        .add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.DNSName("*.localhost"),
                x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
            ]),
            critical=False,
        )
        .add_extension(
            x509.BasicConstraints(ca=False, path_length=None),
            critical=True,
        )
        .sign(private_key, hashes.SHA256())
    )

    # Save private key
    with open("key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))

    # Save certificate
    with open("cert.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    print("Generated key.pem and cert.pem")

Generate Certificate Signing Request (CSR)
------------------------------------------

A CSR is sent to a Certificate Authority to obtain a signed certificate. It
contains your public key and identity information. The CA verifies your identity
and returns a signed certificate. Keep your private key secret—never send it
to the CA.

.. code-block:: python

    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization

    # Generate private key (keep this secret!)
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )

    # Build CSR
    csr = (
        x509.CertificateSigningRequestBuilder()
        .subject_name(x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "My Company"),
            x509.NameAttribute(NameOID.COMMON_NAME, "www.example.com"),
        ]))
        .add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("www.example.com"),
                x509.DNSName("example.com"),
                x509.DNSName("api.example.com"),
            ]),
            critical=False,
        )
        .sign(private_key, hashes.SHA256())
    )

    # Save private key
    with open("private.key", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))

    # Save CSR (send this to CA)
    with open("request.csr", "wb") as f:
        f.write(csr.public_bytes(serialization.Encoding.PEM))

    print("Generated private.key and request.csr")
    print("Send request.csr to your CA, keep private.key secret!")

Read Certificate Information
----------------------------

Parse and inspect X.509 certificates to view subject, issuer, validity period,
extensions, and other attributes. Useful for debugging certificate issues.

.. code-block:: python

    from cryptography import x509
    from cryptography.hazmat.primitives import serialization

    # Load certificate from file
    with open("cert.pem", "rb") as f:
        cert = x509.load_pem_x509_certificate(f.read())

    # Basic information
    print(f"Subject: {cert.subject}")
    print(f"Issuer: {cert.issuer}")
    print(f"Serial: {cert.serial_number}")
    print(f"Not Before: {cert.not_valid_before}")
    print(f"Not After: {cert.not_valid_after}")

    # Get specific subject attributes
    cn = cert.subject.get_attributes_for_oid(x509.oid.NameOID.COMMON_NAME)
    if cn:
        print(f"Common Name: {cn[0].value}")

    # Check extensions
    try:
        san = cert.extensions.get_extension_for_oid(
            x509.oid.ExtensionOID.SUBJECT_ALTERNATIVE_NAME
        )
        print(f"SANs: {san.value.get_values_for_type(x509.DNSName)}")
    except x509.ExtensionNotFound:
        print("No SAN extension")

    # Check if self-signed
    is_self_signed = cert.subject == cert.issuer
    print(f"Self-signed: {is_self_signed}")

    # Verify certificate signature (self-signed only)
    if is_self_signed:
        public_key = cert.public_key()
        try:
            # This verifies the certificate was signed by its own key
            public_key.verify(
                cert.signature,
                cert.tbs_certificate_bytes,
                cert.signature_algorithm_parameters,
            )
            print("Signature valid")
        except Exception as e:
            print(f"Signature invalid: {e}")

Create a Certificate Authority
------------------------------

For internal use, you can create your own CA to sign certificates. The CA
certificate is distributed to clients, which then trust any certificate signed
by the CA. This is useful for development environments or internal services.

.. code-block:: python

    import ipaddress
    from datetime import datetime, timedelta
    from cryptography import x509
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization

    def create_ca():
        """Create a Certificate Authority."""
        # Generate CA private key
        ca_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
        )

        # CA certificate (self-signed)
        ca_name = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "My Internal CA"),
            x509.NameAttribute(NameOID.COMMON_NAME, "My Internal Root CA"),
        ])

        ca_cert = (
            x509.CertificateBuilder()
            .subject_name(ca_name)
            .issuer_name(ca_name)
            .public_key(ca_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.utcnow())
            .not_valid_after(datetime.utcnow() + timedelta(days=3650))  # 10 years
            .add_extension(
                x509.BasicConstraints(ca=True, path_length=0),
                critical=True,
            )
            .add_extension(
                x509.KeyUsage(
                    digital_signature=True,
                    key_cert_sign=True,
                    crl_sign=True,
                    key_encipherment=False,
                    content_commitment=False,
                    data_encipherment=False,
                    key_agreement=False,
                    encipher_only=False,
                    decipher_only=False,
                ),
                critical=True,
            )
            .sign(ca_key, hashes.SHA256())
        )

        return ca_key, ca_cert

    def sign_csr(ca_key, ca_cert, csr_path, days=365):
        """Sign a CSR with the CA."""
        with open(csr_path, "rb") as f:
            csr = x509.load_pem_x509_csr(f.read())

        cert = (
            x509.CertificateBuilder()
            .subject_name(csr.subject)
            .issuer_name(ca_cert.subject)
            .public_key(csr.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(datetime.utcnow())
            .not_valid_after(datetime.utcnow() + timedelta(days=days))
            .add_extension(
                x509.BasicConstraints(ca=False, path_length=None),
                critical=True,
            )
        )

        # Copy extensions from CSR
        for ext in csr.extensions:
            cert = cert.add_extension(ext.value, ext.critical)

        return cert.sign(ca_key, hashes.SHA256())

    # Create CA
    ca_key, ca_cert = create_ca()

    # Save CA files
    with open("ca-key.pem", "wb") as f:
        f.write(ca_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(b"ca-password"),
        ))

    with open("ca-cert.pem", "wb") as f:
        f.write(ca_cert.public_bytes(serialization.Encoding.PEM))

    print("Created ca-key.pem (keep secret!) and ca-cert.pem (distribute to clients)")

TLS Version and Cipher Information
----------------------------------

Inspect TLS connection details including protocol version, cipher suite, and
peer certificate. Useful for debugging and security auditing.

.. code-block:: python

    import ssl
    import socket

    def get_tls_info(hostname, port=443):
        """Get TLS connection information for a host."""
        context = ssl.create_default_context()

        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                print(f"TLS Version: {ssock.version()}")
                print(f"Cipher: {ssock.cipher()}")

                # Peer certificate
                cert = ssock.getpeercert()
                print(f"Subject: {dict(x[0] for x in cert['subject'])}")
                print(f"Issuer: {dict(x[0] for x in cert['issuer'])}")
                print(f"Not Before: {cert['notBefore']}")
                print(f"Not After: {cert['notAfter']}")

                # Subject Alternative Names
                if 'subjectAltName' in cert:
                    sans = [x[1] for x in cert['subjectAltName']]
                    print(f"SANs: {sans}")

    get_tls_info("www.google.com")

Certificate Pinning
-------------------

Certificate pinning adds an extra layer of security by verifying the server's
certificate matches an expected value. This prevents attacks using fraudulently
issued certificates. Pin the public key (SPKI) rather than the certificate to
survive certificate renewals.

.. code-block:: python

    import ssl
    import socket
    import hashlib
    from cryptography import x509
    from cryptography.hazmat.primitives import serialization

    def get_certificate_pin(hostname, port=443):
        """Get the SPKI pin for a certificate."""
        context = ssl.create_default_context()

        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # Get certificate in DER format
                der_cert = ssock.getpeercert(binary_form=True)

        # Parse certificate
        cert = x509.load_der_x509_certificate(der_cert)

        # Get public key in DER format (SPKI)
        spki = cert.public_key().public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        # SHA-256 hash of SPKI
        pin = hashlib.sha256(spki).digest()
        return pin

    def verify_pin(hostname, expected_pin, port=443):
        """Verify certificate matches expected pin."""
        actual_pin = get_certificate_pin(hostname, port)
        if actual_pin != expected_pin:
            raise ssl.SSLError(f"Certificate pin mismatch for {hostname}")
        print(f"Pin verified for {hostname}")

    # Get pin (do this once, store the result)
    pin = get_certificate_pin("www.google.com")
    print(f"Pin (base64): {__import__('base64').b64encode(pin).decode()}")

    # Verify pin on subsequent connections
    verify_pin("www.google.com", pin)
