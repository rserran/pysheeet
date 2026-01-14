.. meta::
    :description lang=en: Modern Python cryptography guide covering symmetric encryption (AES-GCM), asymmetric encryption (RSA-OAEP), digital signatures, key derivation, and secure random generation using the cryptography library
    :keywords: Python, Python3, Cryptography, AES-GCM, RSA, OAEP, Digital Signature, PBKDF2, Argon2, Key Derivation, Encryption, Decryption, HMAC, Hashing

===================
Modern Cryptography
===================

.. contents:: Table of Contents
    :backlinks: none

This guide covers modern cryptographic practices in Python using the ``cryptography``
library, which is the recommended choice for new projects. The library provides both
high-level recipes (Fernet) for common use cases and low-level primitives for advanced
needs. We focus on secure defaults: AES-GCM for symmetric encryption (provides both
confidentiality and integrity), RSA-OAEP for asymmetric encryption, Ed25519 for
signatures, and proper key derivation functions. Avoid deprecated libraries like
PyCrypto—use ``cryptography`` or ``PyCryptodome`` instead.

.. warning::

    Cryptography is difficult to implement correctly. Prefer high-level APIs like
    Fernet when possible. Never invent your own cryptographic schemes. Always use
    authenticated encryption (AES-GCM, ChaCha20-Poly1305) instead of unauthenticated
    modes (AES-CBC, AES-CTR alone).

Algorithm Recommendations
-------------------------

Quick reference for choosing secure algorithms. When in doubt, use the recommended
options—they represent current best practices as of 2024.

::

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                    ALGORITHM RECOMMENDATIONS                            │
    ├─────────────────────────────────────────────────────────────────────────┤
    │  USE CASE              │ RECOMMENDED          │ AVOID                   │
    ├────────────────────────┼──────────────────────┼─────────────────────────┤
    │  Symmetric Encryption  │ AES-256-GCM          │ AES-CBC, AES-ECB,       │
    │                        │ ChaCha20-Poly1305    │ DES, 3DES, Blowfish,    │
    │                        │                      │ RC4                     │
    ├────────────────────────┼──────────────────────┼─────────────────────────┤
    │  Asymmetric Encryption │ RSA-OAEP (≥3072-bit) │ RSA PKCS#1 v1.5,        │
    │                        │ ECIES                │ RSA < 2048-bit,         │
    │                        │                      │ ElGamal                 │
    ├────────────────────────┼──────────────────────┼─────────────────────────┤
    │  Digital Signatures    │ Ed25519              │ RSA PKCS#1 v1.5,        │
    │                        │ RSA-PSS (≥3072-bit)  │ DSA, ECDSA with P-256   │
    │                        │ Ed448                │ (if possible)           │
    ├────────────────────────┼──────────────────────┼─────────────────────────┤
    │  Key Exchange          │ X25519               │ DH < 2048-bit,          │
    │                        │ X448                 │ Static DH               │
    │                        │ ECDH (P-384+)        │                         │
    ├────────────────────────┼──────────────────────┼─────────────────────────┤
    │  Password Hashing      │ Argon2id             │ MD5, SHA-1, SHA-256,    │
    │                        │ scrypt               │ bcrypt (less preferred),│
    │                        │ PBKDF2 (≥600k iter)  │ plain hashes            │
    ├────────────────────────┼──────────────────────┼─────────────────────────┤
    │  General Hashing       │ SHA-256, SHA-3       │ MD5, SHA-1              │
    │                        │ BLAKE2, BLAKE3       │                         │
    ├────────────────────────┼──────────────────────┼─────────────────────────┤
    │  MAC                   │ HMAC-SHA256          │ HMAC-MD5, HMAC-SHA1     │
    │                        │ KMAC, Poly1305       │                         │
    ├────────────────────────┼──────────────────────┼─────────────────────────┤
    │  Random Generation     │ secrets module       │ random module           │
    │                        │ os.urandom()         │ time-based seeds        │
    └────────────────────────┴──────────────────────┴─────────────────────────┘

Key Size Recommendations
------------------------

Minimum key sizes for security through 2030+. Larger keys provide more security
margin but slower performance.

::

    ┌─────────────────────────────────────────────────────────────────────────┐
    │                       KEY SIZE GUIDELINES                               │
    ├─────────────────────────────────────────────────────────────────────────┤
    │  ALGORITHM             │ MINIMUM    │ RECOMMENDED  │ NOTES              │
    ├────────────────────────┼────────────┼──────────────┼────────────────────┤
    │  AES                   │ 128-bit    │ 256-bit      │ 256 for long-term  │
    │  ChaCha20              │ 256-bit    │ 256-bit      │ Only size available│
    │  RSA (encryption)      │ 2048-bit   │ 3072-4096    │ 4096 for long-term │
    │  RSA (signatures)      │ 2048-bit   │ 3072-4096    │ 4096 for long-term │
    │  ECDSA/ECDH            │ P-256      │ P-384        │ Prefer Ed25519     │
    │  Ed25519               │ 256-bit    │ 256-bit      │ Fixed size         │
    │  X25519                │ 256-bit    │ 256-bit      │ Fixed size         │
    │  HMAC key              │ 256-bit    │ 256-bit      │ Match hash output  │
    │  Salt (password)       │ 128-bit    │ 128-bit      │ 16 bytes minimum   │
    │  Nonce (AES-GCM)       │ 96-bit     │ 96-bit       │ 12 bytes, unique!  │
    │  IV (AES-CBC)          │ 128-bit    │ 128-bit      │ 16 bytes, random   │
    └────────────────────────┴────────────┴──────────────┴────────────────────┘

Common Mistakes (Don't Do This)
-------------------------------

Examples of insecure patterns to avoid. Each "BAD" example shows a common mistake;
the "GOOD" example shows the secure alternative.

**❌ Using random module for security:**

.. code-block:: python

    # BAD: Predictable random - can be reverse-engineered!
    import random
    token = ''.join(random.choices('abcdef0123456789', k=32))
    key = bytes([random.randint(0, 255) for _ in range(32)])

    # GOOD: Cryptographically secure random
    import secrets
    token = secrets.token_hex(16)
    key = secrets.token_bytes(32)

**❌ Using ECB mode:**

.. code-block:: python

    # BAD: ECB mode reveals patterns in data!
    from Crypto.Cipher import AES
    cipher = AES.new(key, AES.MODE_ECB)  # NEVER use ECB

    # GOOD: Use authenticated encryption
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

**❌ AES-CBC without authentication:**

.. code-block:: python

    # BAD: No integrity check - vulnerable to padding oracle attacks!
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    # Attacker can modify ciphertext without detection!

    # GOOD: AES-GCM provides authentication
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    # Any modification will be detected during decryption

**❌ Reusing nonces:**

.. code-block:: python

    # BAD: Reusing nonce completely breaks AES-GCM security!
    nonce = b'fixed_nonce!'  # NEVER do this
    ct1 = aesgcm.encrypt(nonce, msg1, None)
    ct2 = aesgcm.encrypt(nonce, msg2, None)  # Catastrophic!

    # GOOD: Generate unique nonce for each encryption
    import os
    nonce1 = os.urandom(12)
    ct1 = aesgcm.encrypt(nonce1, msg1, None)
    nonce2 = os.urandom(12)
    ct2 = aesgcm.encrypt(nonce2, msg2, None)

**❌ RSA with PKCS#1 v1.5 padding:**

.. code-block:: python

    # BAD: Vulnerable to Bleichenbacher's attack!
    from Crypto.Cipher import PKCS1_v1_5
    cipher = PKCS1_v1_5.new(key)
    ciphertext = cipher.encrypt(message)

    # GOOD: Use OAEP padding
    from cryptography.hazmat.primitives.asymmetric import padding
    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

**❌ Hashing passwords with SHA-256:**

.. code-block:: python

    # BAD: Too fast - billions of guesses per second!
    import hashlib
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # GOOD: Use slow password hashing function
    from argon2 import PasswordHasher
    ph = PasswordHasher()
    password_hash = ph.hash(password)

**❌ Comparing MACs with ==:**

.. code-block:: python

    # BAD: Timing attack reveals information about correct MAC!
    if received_mac == computed_mac:  # VULNERABLE
        process_message()

    # GOOD: Constant-time comparison
    import hmac
    if hmac.compare_digest(received_mac, computed_mac):
        process_message()

**❌ Hardcoding keys/secrets:**

.. code-block:: python

    # BAD: Keys in source code end up in version control!
    SECRET_KEY = "super_secret_key_12345"
    API_KEY = "ak_live_xxxxxxxxxxxxx"

    # GOOD: Use environment variables or secret management
    import os
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # Or use: AWS Secrets Manager, HashiCorp Vault, etc.

Security Checklist
------------------

Use this checklist when implementing cryptography in your application.

**Before You Start:**

.. code-block:: text

    □ Do I really need custom crypto? (Consider existing solutions first)
    □ Am I using a well-maintained library? (cryptography, not PyCrypto)
    □ Have I read the library's security documentation?

**Key Management:**

.. code-block:: text

    □ Keys generated with cryptographically secure random (secrets/os.urandom)
    □ Keys are appropriate size (AES-256, RSA ≥3072-bit)
    □ Keys stored securely (not in source code, use env vars or secret manager)
    □ Key rotation plan in place
    □ Different keys for different purposes (encryption vs signing)
    □ Keys protected at rest (encrypted with master key or HSM)

**Encryption:**

.. code-block:: text

    □ Using authenticated encryption (AES-GCM or ChaCha20-Poly1305)
    □ Nonces are unique per encryption (random 12 bytes for AES-GCM)
    □ Not reusing key+nonce combinations
    □ Associated data (AAD) used where appropriate
    □ Ciphertext includes nonce for decryption
    □ Using RSA-OAEP (not PKCS#1 v1.5) for asymmetric encryption

**Signatures:**

.. code-block:: text

    □ Using Ed25519 or RSA-PSS (not PKCS#1 v1.5)
    □ Signing the right data (include all relevant fields)
    □ Verifying signatures before trusting data
    □ Handling verification failures securely

**Password Storage:**

.. code-block:: text

    □ Using Argon2id, scrypt, or PBKDF2 (not plain hashes)
    □ Unique salt per password (≥16 bytes)
    □ Sufficient iterations/memory cost (tune for ~100ms-500ms)
    □ Rehashing when parameters change
    □ Not logging passwords or hashes

**TLS/Network:**

.. code-block:: text

    □ TLS 1.2 or 1.3 only (no SSL, TLS 1.0, TLS 1.1)
    □ Certificate validation enabled
    □ Using trusted CA certificates
    □ Hostname verification enabled
    □ Certificate pinning for high-security apps

**General:**

.. code-block:: text

    □ No sensitive data in logs
    □ Secure memory handling (clear keys after use where possible)
    □ Error messages don't leak sensitive information
    □ Timing-safe comparisons for secrets
    □ Dependencies up to date (check for CVEs)

Secure Random Generation
------------------------

Cryptographic operations require unpredictable random numbers. Python's ``secrets``
module (Python 3.6+) provides cryptographically secure random generation, suitable
for tokens, passwords, and keys. Never use the ``random`` module for security-sensitive
applications—it uses a predictable PRNG (Mersenne Twister) that can be reverse-engineered
from observed outputs.

.. code-block:: python

    import secrets
    import os

    # Generate random bytes (for keys, IVs, salts)
    key = secrets.token_bytes(32)      # 256-bit key
    iv = secrets.token_bytes(16)       # 128-bit IV

    # Generate URL-safe token (for session IDs, API keys)
    token = secrets.token_urlsafe(32)  # ~43 characters

    # Generate hex token
    hex_token = secrets.token_hex(16)  # 32 hex characters

    # Secure random integer
    n = secrets.randbelow(100)         # 0 <= n < 100

    # Secure choice from sequence
    password_char = secrets.choice('abcdefghijklmnopqrstuvwxyz0123456789')

    # Alternative: os.urandom (works on all Python versions)
    key = os.urandom(32)

Cryptographic Hashing
---------------------

Hash functions produce fixed-size digests from arbitrary data. Use SHA-256 or SHA-3
for general hashing. For password storage, use dedicated password hashing functions
(see Key Derivation section). Hash functions are one-way: you cannot recover the
original data from a hash. They're used for data integrity verification, digital
signatures, and as building blocks for other cryptographic operations.

.. code-block:: python

    import hashlib

    data = b"Hello, World!"

    # SHA-256 (recommended for general use)
    digest = hashlib.sha256(data).hexdigest()
    print(f"SHA-256: {digest}")

    # SHA-3 (newer, different internal structure)
    digest = hashlib.sha3_256(data).hexdigest()
    print(f"SHA3-256: {digest}")

    # BLAKE2 (fast, secure, supports keying)
    digest = hashlib.blake2b(data, digest_size=32).hexdigest()
    print(f"BLAKE2b: {digest}")

    # Keyed BLAKE2 (MAC without separate HMAC construction)
    key = b"secret-key-here!"
    mac = hashlib.blake2b(data, key=key, digest_size=32).hexdigest()

    # Incremental hashing (for large files)
    h = hashlib.sha256()
    with open("largefile.bin", "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    print(f"File hash: {h.hexdigest()}")

HMAC (Hash-based Message Authentication Code)
---------------------------------------------

HMAC provides message authentication—verifying both integrity and authenticity.
Unlike plain hashes, HMAC requires a secret key, so only parties with the key can
create or verify the MAC. Use HMAC when you need to ensure data hasn't been tampered
with and came from someone who knows the secret. Always use constant-time comparison
to prevent timing attacks when verifying MACs.

.. code-block:: python

    import hmac
    import hashlib
    import secrets

    key = secrets.token_bytes(32)
    message = b"Important message"

    # Create HMAC
    mac = hmac.new(key, message, hashlib.sha256).digest()

    # Verify HMAC (constant-time comparison)
    received_mac = mac  # In practice, received from sender
    if hmac.compare_digest(mac, received_mac):
        print("Message is authentic")
    else:
        print("Message was tampered with!")

    # HMAC with hexdigest
    mac_hex = hmac.new(key, message, hashlib.sha256).hexdigest()

Key Derivation Functions
------------------------

Key derivation functions (KDFs) derive cryptographic keys from passwords or other
key material. For passwords, use slow KDFs (PBKDF2, Argon2, scrypt) that resist
brute-force attacks. For deriving multiple keys from a master key, use HKDF. Never
use plain hashes (SHA-256) for password storage—they're too fast, allowing billions
of guesses per second.

.. code-block:: python

    import os
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

    # PBKDF2 - widely supported, use >= 600,000 iterations (OWASP 2023)
    password = b"user-password"
    salt = os.urandom(16)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600_000,
    )
    key = kdf.derive(password)

    # To verify a password, derive again and compare
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,  # Must use same salt
        iterations=600_000,
    )
    try:
        kdf.verify(password, key)
        print("Password correct")
    except Exception:
        print("Password incorrect")

    # Scrypt - memory-hard, better resistance to GPU/ASIC attacks
    kdf = Scrypt(salt=salt, length=32, n=2**17, r=8, p=1)
    key = kdf.derive(password)

    # HKDF - for deriving multiple keys from master key (not for passwords)
    master_key = os.urandom(32)
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=b"encryption-key",
    )
    derived_key = hkdf.derive(master_key)

Symmetric Encryption: AES-GCM
-----------------------------

AES-GCM (Galois/Counter Mode) is the recommended symmetric encryption mode. It
provides authenticated encryption: both confidentiality (data is encrypted) and
integrity (tampering is detected). The authentication tag ensures ciphertext hasn't
been modified. Always use a unique nonce (number used once) for each encryption
with the same key—reusing nonces completely breaks security.

::

    ┌─────────────────────────────────────────────────────────────────┐
    │                     AES-GCM ENCRYPTION                          │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │   Plaintext ──┬──► AES-GCM ──► Ciphertext                       │
    │               │       │                                         │
    │   Key ────────┤       ├──► Authentication Tag (16 bytes)        │
    │               │       │                                         │
    │   Nonce ──────┘       └──► Associated Data (AAD) authenticated  │
    │   (12 bytes)                but not encrypted                   │
    │                                                                 │
    │   Security: Nonce MUST be unique per key. Random 12-byte        │
    │   nonce is safe for ~2^32 encryptions per key.                  │
    │                                                                 │
    └─────────────────────────────────────────────────────────────────┘

.. code-block:: python

    import os
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    # Generate a random 256-bit key
    key = AESGCM.generate_key(bit_length=256)

    # Create cipher
    aesgcm = AESGCM(key)

    # Encrypt
    nonce = os.urandom(12)  # 96-bit nonce, MUST be unique per encryption
    plaintext = b"Secret message"
    associated_data = b"header"  # Authenticated but not encrypted (optional)

    ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data)
    # ciphertext includes the 16-byte authentication tag

    # Decrypt
    decrypted = aesgcm.decrypt(nonce, ciphertext, associated_data)
    assert decrypted == plaintext

    # Tampering detection - modifying ciphertext raises exception
    try:
        tampered = bytearray(ciphertext)
        tampered[0] ^= 1  # Flip one bit
        aesgcm.decrypt(nonce, bytes(tampered), associated_data)
    except Exception as e:
        print(f"Tampering detected: {e}")

Symmetric Encryption: ChaCha20-Poly1305
---------------------------------------

ChaCha20-Poly1305 is an alternative to AES-GCM, offering similar security with
better performance on systems without AES hardware acceleration (common on mobile
devices and older CPUs). It's used by TLS 1.3, WireGuard, and many modern protocols.
Like AES-GCM, it provides authenticated encryption with associated data (AEAD).

.. code-block:: python

    import os
    from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

    # Generate key (256-bit)
    key = ChaCha20Poly1305.generate_key()

    # Create cipher
    chacha = ChaCha20Poly1305(key)

    # Encrypt
    nonce = os.urandom(12)  # 96-bit nonce
    plaintext = b"Secret message"
    aad = b"additional authenticated data"

    ciphertext = chacha.encrypt(nonce, plaintext, aad)

    # Decrypt
    decrypted = chacha.decrypt(nonce, ciphertext, aad)
    assert decrypted == plaintext

High-Level Encryption: Fernet
-----------------------------

Fernet provides a high-level, easy-to-use symmetric encryption API. It uses AES-128-CBC
with HMAC for authentication, handles IV generation, and includes timestamp for
optional TTL-based expiration. Use Fernet when you need simple, secure encryption
without worrying about low-level details. The downside is slightly larger ciphertext
and no associated data support.

.. code-block:: python

    from cryptography.fernet import Fernet, InvalidToken
    import time

    # Generate key (store this securely!)
    key = Fernet.generate_key()
    print(f"Key: {key.decode()}")  # Base64-encoded

    # Create Fernet instance
    f = Fernet(key)

    # Encrypt
    plaintext = b"Secret message"
    token = f.encrypt(plaintext)
    print(f"Token: {token.decode()}")

    # Decrypt
    decrypted = f.decrypt(token)
    assert decrypted == plaintext

    # Decrypt with TTL (time-to-live in seconds)
    try:
        # Token must have been created within last 60 seconds
        decrypted = f.decrypt(token, ttl=60)
    except InvalidToken:
        print("Token expired or invalid")

    # Key rotation with MultiFernet
    from cryptography.fernet import MultiFernet

    old_key = Fernet.generate_key()
    new_key = Fernet.generate_key()

    # MultiFernet tries keys in order for decryption
    # Always encrypts with first key
    multi = MultiFernet([Fernet(new_key), Fernet(old_key)])

    # Can decrypt tokens from either key
    old_token = Fernet(old_key).encrypt(b"old data")
    decrypted = multi.decrypt(old_token)  # Works!

    # Re-encrypt with new key
    new_token = multi.rotate(old_token)

RSA Key Generation
------------------

RSA is an asymmetric algorithm using public/private key pairs. The public key
encrypts data or verifies signatures; the private key decrypts or signs. Modern
recommendations: use at least 2048-bit keys (3072 or 4096 for long-term security),
public exponent 65537, and OAEP padding for encryption or PSS for signatures.
For new systems, consider Ed25519 (signatures) or X25519 (key exchange) instead.

.. code-block:: python

    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization

    # Generate RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,  # 2048 minimum, 4096 for long-term
    )
    public_key = private_key.public_key()

    # Serialize private key (PEM format)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase"),
    )

    # Serialize private key without encryption
    private_pem_unencrypted = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    # Serialize public key
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    # Save to files
    with open("private_key.pem", "wb") as f:
        f.write(private_pem)
    with open("public_key.pem", "wb") as f:
        f.write(public_pem)

    # Load keys from files
    with open("private_key.pem", "rb") as f:
        loaded_private = serialization.load_pem_private_key(
            f.read(),
            password=b"passphrase",
        )

    with open("public_key.pem", "rb") as f:
        loaded_public = serialization.load_pem_public_key(f.read())

RSA Encryption (OAEP)
---------------------

RSA encryption should always use OAEP (Optimal Asymmetric Encryption Padding).
Never use PKCS#1 v1.5 padding for new applications—it's vulnerable to padding
oracle attacks. RSA can only encrypt small amounts of data (key_size/8 - padding
overhead), so it's typically used to encrypt a symmetric key, which then encrypts
the actual data (hybrid encryption).

::

    ┌─────────────────────────────────────────────────────────────────┐
    │                    RSA-OAEP ENCRYPTION                          │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │   Plaintext ──► OAEP Padding ──► RSA ──► Ciphertext             │
    │                      │            │                             │
    │                      │      Public Key                          │
    │                      │                                          │
    │   OAEP uses:                                                    │
    │   - MGF1 (Mask Generation Function)                             │
    │   - Hash algorithm (SHA-256 recommended)                        │
    │   - Optional label                                              │
    │                                                                 │
    │   Max plaintext size: key_bytes - 2*hash_bytes - 2              │
    │   For 4096-bit key with SHA-256: 512 - 64 - 2 = 446 bytes       │
    │                                                                 │
    └─────────────────────────────────────────────────────────────────┘

.. code-block:: python

    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives import hashes

    # Generate keys
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
    public_key = private_key.public_key()

    # Encrypt with public key (OAEP padding)
    plaintext = b"Secret message for RSA"
    ciphertext = public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    # Decrypt with private key
    decrypted = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    assert decrypted == plaintext

Hybrid Encryption
-----------------

RSA has size limits and is slow. Hybrid encryption combines RSA's key distribution
benefits with symmetric encryption's speed: generate a random symmetric key, encrypt
the data with AES-GCM, then encrypt the symmetric key with RSA. The recipient
decrypts the symmetric key with their RSA private key, then decrypts the data.

.. code-block:: python

    import os
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    def hybrid_encrypt(public_key, plaintext):
        """Encrypt data using hybrid RSA + AES-GCM."""
        # Generate random AES key and nonce
        aes_key = AESGCM.generate_key(bit_length=256)
        nonce = os.urandom(12)

        # Encrypt data with AES-GCM
        aesgcm = AESGCM(aes_key)
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)

        # Encrypt AES key with RSA-OAEP
        encrypted_key = public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        return encrypted_key, nonce, ciphertext

    def hybrid_decrypt(private_key, encrypted_key, nonce, ciphertext):
        """Decrypt data using hybrid RSA + AES-GCM."""
        # Decrypt AES key with RSA
        aes_key = private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        # Decrypt data with AES-GCM
        aesgcm = AESGCM(aes_key)
        return aesgcm.decrypt(nonce, ciphertext, None)

    # Usage
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
    public_key = private_key.public_key()

    message = b"This message can be arbitrarily long!" * 1000
    encrypted_key, nonce, ciphertext = hybrid_encrypt(public_key, message)
    decrypted = hybrid_decrypt(private_key, encrypted_key, nonce, ciphertext)
    assert decrypted == message

Digital Signatures: RSA-PSS
---------------------------

Digital signatures prove authenticity and integrity. The signer uses their private
key to create a signature; anyone with the public key can verify it. Use PSS
(Probabilistic Signature Scheme) padding for RSA signatures—it's provably secure
unlike PKCS#1 v1.5. For new applications, consider Ed25519 instead of RSA.

.. code-block:: python

    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives import hashes

    # Generate keys
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
    public_key = private_key.public_key()

    message = b"Message to sign"

    # Sign with private key (PSS padding)
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )

    # Verify with public key
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        print("Signature valid")
    except Exception:
        print("Signature invalid!")

Digital Signatures: Ed25519
---------------------------

Ed25519 is a modern signature algorithm based on elliptic curves. It offers
excellent security with small keys (32 bytes) and signatures (64 bytes), fast
operations, and resistance to many implementation pitfalls. Prefer Ed25519 over
RSA for new applications unless you need compatibility with legacy systems.

.. code-block:: python

    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives import serialization

    # Generate key pair
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    # Sign message
    message = b"Message to sign"
    signature = private_key.sign(message)

    # Verify signature
    try:
        public_key.verify(signature, message)
        print("Signature valid")
    except Exception:
        print("Signature invalid!")

    # Serialize keys
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    # OpenSSH format for public key
    public_ssh = public_key.public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH,
    )
    print(public_ssh.decode())  # ssh-ed25519 AAAA...

Elliptic Curve Diffie-Hellman (ECDH)
------------------------------------

ECDH allows two parties to establish a shared secret over an insecure channel.
Each party generates a key pair, exchanges public keys, and derives the same
shared secret. Use X25519 (Curve25519) for modern applications—it's fast, secure,
and resistant to timing attacks. The shared secret should be passed through a KDF
before use as an encryption key.

.. code-block:: python

    from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from cryptography.hazmat.primitives import hashes

    # Alice generates her key pair
    alice_private = X25519PrivateKey.generate()
    alice_public = alice_private.public_key()

    # Bob generates his key pair
    bob_private = X25519PrivateKey.generate()
    bob_public = bob_private.public_key()

    # Exchange public keys (over insecure channel)
    # Alice computes shared secret
    alice_shared = alice_private.exchange(bob_public)

    # Bob computes shared secret
    bob_shared = bob_private.exchange(alice_public)

    # Both arrive at the same shared secret
    assert alice_shared == bob_shared

    # Derive encryption key from shared secret using HKDF
    def derive_key(shared_secret, info):
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=info,
        )
        return hkdf.derive(shared_secret)

    encryption_key = derive_key(alice_shared, b"encryption")
    mac_key = derive_key(alice_shared, b"authentication")

Password Hashing with Argon2
----------------------------

Argon2 is the winner of the Password Hashing Competition (2015) and the recommended
algorithm for password storage. It's memory-hard, making GPU/ASIC attacks expensive.
Use the ``argon2-cffi`` library for Python. Store the full hash string (includes
salt and parameters) in your database.

.. code-block:: python

    # pip install argon2-cffi
    from argon2 import PasswordHasher
    from argon2.exceptions import VerifyMismatchError

    ph = PasswordHasher(
        time_cost=3,        # Number of iterations
        memory_cost=65536,  # Memory usage in KiB (64 MB)
        parallelism=4,      # Number of parallel threads
    )

    # Hash a password (for storage)
    password = "user-password"
    hash_str = ph.hash(password)
    print(f"Hash: {hash_str}")
    # $argon2id$v=19$m=65536,t=3,p=4$...

    # Verify a password (during login)
    try:
        ph.verify(hash_str, password)
        print("Password correct")

        # Check if rehash needed (parameters changed)
        if ph.check_needs_rehash(hash_str):
            new_hash = ph.hash(password)
            # Update stored hash
    except VerifyMismatchError:
        print("Password incorrect")
