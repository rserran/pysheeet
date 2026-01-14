.. meta::
    :description lang=en: Python cryptography tutorial covering AES-GCM encryption, RSA, digital signatures, key derivation, TLS/SSL, and certificate management
    :keywords: Python, Python3, cryptography, encryption, AES, RSA, TLS, SSL, certificate, HTTPS, digital signature, key derivation, Argon2

============
Cryptography
============

Cryptography is essential for securing data in transit and at rest. This section
covers modern cryptographic practices in Python using well-maintained libraries
like ``cryptography`` and ``argon2-cffi``. We emphasize secure defaults: authenticated
encryption (AES-GCM), proper key derivation (PBKDF2, Argon2), secure signatures
(Ed25519, RSA-PSS), and correct TLS configuration. Avoid deprecated libraries
(PyCrypto) and insecure patterns (AES-CBC without authentication, PKCS#1 v1.5
padding, MD5/SHA1 for security purposes).

.. toctree::
    :maxdepth: 1

    python-crypto
    python-tls
