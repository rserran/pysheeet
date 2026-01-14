.. meta::
    :description lang=en: Python security and cryptography guide covering modern encryption, TLS/SSL, common vulnerabilities, and secure coding practices
    :keywords: Python, Python3, security, cryptography, encryption, AES, RSA, TLS, SSL, vulnerability, padding oracle, injection, secure coding

========
Security
========

Security is essential for protecting data in transit and at rest. This section
covers modern cryptographic practices using well-maintained libraries like
``cryptography`` and ``argon2-cffi``, as well as common security vulnerabilities
and how to avoid them. We emphasize secure defaults: authenticated encryption
(AES-GCM), proper key derivation (PBKDF2, Argon2), secure signatures (Ed25519,
RSA-PSS), and correct TLS configuration.

Understanding vulnerabilities is equally important—knowing why legacy patterns
like AES-CBC without authentication or PKCS#1 v1.5 padding are dangerous helps
you recognize and fix insecure code in existing systems.

.. toctree::
    :maxdepth: 1

    python-crypto
    python-tls
    python-vulnerability
