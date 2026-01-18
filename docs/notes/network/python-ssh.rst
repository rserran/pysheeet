.. meta::
    :description lang=en: Comprehensive SSH cheat sheet for Python developers covering Paramiko library, SSH tunneling (local, reverse, dynamic), port forwarding, SFTP file transfers, jump hosts, and key management with practical examples
    :keywords: Python, Python3, SSH, Paramiko, SFTP, SSH Tunnel, Port Forwarding, Reverse Tunnel, Jump Host, ProxyJump, Bastion Host, SOCKS Proxy, SSH Agent, Key Authentication, Remote Execution

======================
SSH and Secure Tunnels
======================

.. contents:: Table of Contents
    :backlinks: none

SSH (Secure Shell) is the standard protocol for secure remote access, providing
encrypted communication between machines for command execution, file transfer,
and network tunneling. Originally developed as a secure replacement for telnet
and rsh, SSH has become essential infrastructure for system administration,
deployment automation, and secure network access. Python's ``paramiko`` library
provides a complete implementation of SSHv2 protocol, enabling programmatic SSH
connections, SFTP file transfers, and sophisticated port forwarding scenarios.
This cheat sheet covers the full spectrum of SSH operations—from basic password
and key authentication to advanced tunneling techniques like reverse tunnels for
NAT traversal, jump hosts for accessing isolated networks, and dynamic SOCKS
proxies for routing arbitrary traffic through secure channels.

Basic SSH Connection
--------------------

The foundation of SSH is establishing a secure, authenticated connection to a
remote host. The ``SSHClient`` class in Paramiko manages the entire connection
lifecycle including TCP connection, cryptographic handshake, host key verification,
user authentication, and channel multiplexing. Once connected, you can execute
commands, open interactive shells, or establish SFTP sessions. The context manager
pattern (``with`` statement) ensures connections are properly closed even if
exceptions occur, preventing resource leaks in long-running applications.

.. code-block:: python

    from paramiko.client import SSHClient

    # Basic password authentication
    with SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.connect("example.com", username="user", password="secret")
        stdin, stdout, stderr = ssh.exec_command("uname -a")
        print(stdout.read().decode())

.. code-block:: python

    # Connect on non-standard port
    with SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.connect("example.com", port=2222, username="user", password="secret")
        stdin, stdout, stderr = ssh.exec_command("hostname")
        print(stdout.read().decode())

Host Key Verification
---------------------

SSH's security model relies on verifying the server's identity before sending
credentials. Each SSH server has a unique host key pair, and clients store known
host public keys in ``~/.ssh/known_hosts``. On first connection, SSH warns about
unknown hosts—this is the "fingerprint" prompt you see. Blindly accepting unknown
keys defeats this protection and enables man-in-the-middle attacks where an
attacker intercepts your connection. For automation, ``AutoAddPolicy`` is
convenient but should only be used in trusted networks or with additional
verification. In production, pre-populate known_hosts or use certificate-based
host authentication.

.. code-block:: python

    import paramiko
    from paramiko.client import SSHClient

    # Auto-add unknown host keys (use cautiously)
    # Equivalent to: ssh -o StrictHostKeyChecking=no
    with SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("example.com", username="user", password="secret")
        stdin, stdout, stderr = ssh.exec_command("whoami")
        print(stdout.read().decode())

    # Reject unknown hosts (default, most secure)
    with SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.RejectPolicy())
        ssh.load_system_host_keys()  # Load ~/.ssh/known_hosts
        ssh.connect("example.com", username="user", password="secret")

Key-Based Authentication
------------------------

SSH key pairs provide significantly stronger security than passwords while
enabling passwordless automation. A key pair consists of a private key (kept
secret on your machine) and a public key (copied to servers you want to access).
Authentication works by proving you possess the private key without transmitting
it. Modern best practice recommends Ed25519 keys for their security and performance,
though RSA (4096-bit) remains widely compatible. Protect private keys with a
passphrase for defense-in-depth—if the key file is stolen, the passphrase provides
an additional barrier. Use ``ssh-agent`` to cache decrypted keys in memory,
avoiding repeated passphrase entry.

.. code-block:: python

    from paramiko.client import SSHClient

    # Using private key file
    # ssh-keygen -t ed25519 -f mykey
    # ssh-copy-id -i mykey.pub user@example.com
    with SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.connect("example.com", username="user", key_filename="mykey")
        stdin, stdout, stderr = ssh.exec_command("id")
        print(stdout.read().decode())

.. code-block:: python

    # Key with passphrase
    with SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.connect(
            "example.com",
            username="user",
            key_filename="mykey",
            passphrase="my-key-passphrase"
        )

.. code-block:: python

    # Using RSAKey object directly
    from paramiko import RSAKey

    pkey = RSAKey.from_private_key_file("mykey", password="passphrase")
    with SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.connect("example.com", username="user", pkey=pkey)

SFTP File Transfer
------------------

SFTP (SSH File Transfer Protocol) runs over an SSH connection, providing secure,
encrypted file operations without requiring a separate service or port. Unlike
FTP which sends credentials in plaintext and requires complex firewall rules for
passive mode, SFTP tunnels everything through the existing SSH connection on port
22. Paramiko's SFTP client supports the full range of file operations: uploading,
downloading, directory listing, file metadata, permissions, and remote file
manipulation. For large transfers, SFTP handles resume and provides progress
callbacks. It's the standard choice for automated file transfers in deployment
scripts, backup systems, and data pipelines where security is required.

.. code-block:: python

    from paramiko.client import SSHClient

    with SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.connect("example.com", username="user", key_filename="mykey")
        sftp = ssh.open_sftp()

        # Upload file
        sftp.put("local_file.txt", "/remote/path/file.txt")

        # Download file
        sftp.get("/remote/path/file.txt", "downloaded.txt")

        # List directory
        for entry in sftp.listdir("/remote/path"):
            print(entry)

        # File operations
        sftp.mkdir("/remote/newdir")
        sftp.rename("/remote/old.txt", "/remote/new.txt")
        sftp.remove("/remote/unwanted.txt")

        # Get file stats
        stat = sftp.stat("/remote/file.txt")
        print(f"Size: {stat.st_size}, Modified: {stat.st_mtime}")

        sftp.close()

SSH Tunneling Overview
----------------------

SSH tunneling (port forwarding) is one of SSH's most powerful features, allowing
you to securely route network traffic through an encrypted SSH connection. This
enables accessing services behind firewalls, encrypting otherwise insecure
protocols, and bypassing network restrictions. There are three types: local
forwarding brings a remote service to your machine, remote (reverse) forwarding
exposes your local service to the remote network, and dynamic forwarding creates
a SOCKS proxy for routing arbitrary traffic. Understanding these patterns is
essential for secure access to databases, internal web applications, and services
in private networks. The diagrams below illustrate the traffic flow for each type.

::

    ┌─────────────────────────────────────────────────────────────────┐
    │                    SSH TUNNEL TYPES                             │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │  LOCAL FORWARDING (-L)                                          │
    │  Access remote service through local port                       │
    │                                                                 │
    │    [You] ──► localhost:8080 ══SSH══► [Server] ──► db:5432       │
    │                                                                 │
    │    ssh -L 8080:database.internal:5432 user@server               │
    │    Then connect to localhost:8080 to reach database             │
    │                                                                 │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │  REMOTE/REVERSE FORWARDING (-R)                                 │
    │  Expose local service to remote server                          │
    │                                                                 │
    │    [You:3000] ◄── [Server]:9000 ◄══SSH══◄ [You initiate]        │
    │                                                                 │
    │    ssh -R 9000:localhost:3000 user@server                       │
    │    Server's port 9000 forwards to your localhost:3000           │
    │                                                                 │
    ├─────────────────────────────────────────────────────────────────┤
    │                                                                 │
    │  DYNAMIC FORWARDING (-D) - SOCKS Proxy                          │
    │  Route any traffic through SSH server                           │
    │                                                                 │
    │    [You] ──► localhost:1080 ══SSH══► [Server] ──► anywhere      │
    │                                                                 │
    │    ssh -D 1080 user@server                                      │
    │    Configure browser/app to use SOCKS5 proxy localhost:1080     │
    │                                                                 │
    └─────────────────────────────────────────────────────────────────┘

Local Port Forwarding
---------------------

Local forwarding (``-L``) is the most common tunnel type, binding a port on your
local machine that forwards traffic through the SSH server to a destination host.
This is invaluable for accessing services in private networks—databases, internal
web applications, admin interfaces—that aren't exposed to the internet. The SSH
server acts as a relay: your local application connects to ``localhost:port``,
SSH encrypts and forwards the traffic to the server, which then connects to the
final destination. The destination doesn't need to be the SSH server itself; it
can be any host reachable from the server, making this perfect for bastion/jump
host scenarios where you SSH to a gateway machine to reach internal resources.

::

    Scenario: Access internal database through bastion host

    ┌──────────┐      ┌──────────────┐      ┌────────────────┐
    │  Your    │ SSH  │   Bastion    │      │   Database     │
    │  Machine │─────►│   Server     │─────►│   (internal)   │
    │          │      │              │      │   db:5432      │
    └──────────┘      └──────────────┘      └────────────────┘
         │
         │ Connect to localhost:5432
         │ Traffic tunneled to db:5432
         ▼

    Command: ssh -L 5432:db.internal:5432 user@bastion
    Then:    psql -h localhost -p 5432 mydb

.. code-block:: python

    # Local port forwarding with Paramiko
    import paramiko
    from paramiko.client import SSHClient
    import socket
    import select
    import threading

    def forward_tunnel(local_port, remote_host, remote_port, ssh_client):
        """Forward local_port to remote_host:remote_port via SSH."""
        transport = ssh_client.get_transport()

        # Create local listening socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('127.0.0.1', local_port))
        server.listen(5)
        print(f"Forwarding localhost:{local_port} -> {remote_host}:{remote_port}")

        while True:
            client, addr = server.accept()
            # Open channel to remote destination
            channel = transport.open_channel(
                'direct-tcpip',
                (remote_host, remote_port),
                client.getpeername()
            )
            if channel is None:
                client.close()
                continue

            # Bidirectional forwarding in thread
            threading.Thread(
                target=_forward_data, args=(client, channel), daemon=True
            ).start()

    def _forward_data(sock, channel):
        """Forward data between socket and SSH channel."""
        while True:
            r, w, x = select.select([sock, channel], [], [])
            if sock in r:
                data = sock.recv(4096)
                if not data:
                    break
                channel.send(data)
            if channel in r:
                data = channel.recv(4096)
                if not data:
                    break
                sock.send(data)
        sock.close()
        channel.close()

    # Usage
    with SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.connect("bastion.example.com", username="user", key_filename="mykey")
        # Forward localhost:5432 to internal-db:5432
        forward_tunnel(5432, "internal-db.local", 5432, ssh)

Reverse Port Forwarding
-----------------------

Reverse forwarding (``-R``) solves the opposite problem: exposing a service on
your local machine to the remote server's network. This is essential when you're
behind NAT, a corporate firewall, or any network that blocks incoming connections.
You initiate an outbound SSH connection (which firewalls typically allow), and
the SSH server opens a listening port that tunnels back to your machine. Common
use cases include sharing a local development server with remote colleagues,
providing temporary access to a local service for debugging, or creating a
"callback" channel when direct inbound connections are impossible. Note that by
default, the server only binds to ``127.0.0.1``; to allow external access, the
server's ``sshd_config`` needs ``GatewayPorts yes``.

::

    Scenario: Expose local dev server to public server

    ┌──────────────┐                    ┌──────────────┐
    │  Your Machine│   SSH Connection   │ Public Server│
    │  (behind NAT)│═══════════════════►│              │
    │              │   You initiate     │              │
    │  localhost   │                    │  0.0.0.0     │
    │    :3000     │◄───────────────────│    :9000     │
    │  (your app)  │   Tunnel back      │  (exposed)   │
    └──────────────┘                    └──────────────┘

    Command: ssh -R 9000:localhost:3000 user@public-server
    Result:  Anyone connecting to public-server:9000
             reaches your localhost:3000

    Note: Server needs "GatewayPorts yes" in sshd_config
          to allow binding to 0.0.0.0 (not just 127.0.0.1)

.. code-block:: python

    # Reverse tunnel with Paramiko
    import paramiko
    from paramiko.client import SSHClient
    import socket
    import select
    import threading

    def reverse_tunnel(server_port, local_host, local_port, ssh_client):
        """Expose local_host:local_port on SSH server's server_port."""
        transport = ssh_client.get_transport()

        # Request remote port forwarding
        transport.request_port_forward('', server_port)
        print(f"Reverse tunnel: server:{server_port} -> {local_host}:{local_port}")

        while True:
            # Accept forwarded connection from server
            channel = transport.accept(1000)
            if channel is None:
                continue

            # Connect to local service
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect((local_host, local_port))
            except Exception as e:
                print(f"Local connection failed: {e}")
                channel.close()
                continue

            # Bidirectional forwarding
            threading.Thread(
                target=_forward_data, args=(sock, channel), daemon=True
            ).start()

    # Usage: Expose local web server on remote port 9000
    with SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.connect("public-server.com", username="user", key_filename="mykey")
        reverse_tunnel(9000, "localhost", 3000, ssh)

Dynamic Port Forwarding (SOCKS Proxy)
-------------------------------------

Dynamic forwarding (``-D``) creates a local SOCKS proxy server that routes traffic
through the SSH connection. Unlike local forwarding where you specify a fixed
destination, dynamic forwarding lets applications connect to any host reachable
from the SSH server—the destination is determined per-connection by the SOCKS
protocol. This is incredibly versatile: configure your browser to use the SOCKS
proxy and all web traffic flows through the SSH server, effectively browsing from
that server's network location. Use cases include accessing geo-restricted content,
browsing internal websites from outside the office, or encrypting traffic on
untrusted networks (coffee shop WiFi). SOCKS5 supports both TCP and UDP, plus
authentication, making it more capable than HTTP proxies.

::

    ┌──────────┐      ┌──────────────┐      ┌─────────────┐
    │  Your    │ SSH  │   SSH        │      │  Any        │
    │  Machine │═════►│   Server     │─────►│  Destination│
    │          │      │              │      │             │
    └──────────┘      └──────────────┘      └─────────────┘
         │
         │ SOCKS5 proxy on localhost:1080
         │ Browser/apps route traffic through it
         ▼

    Command: ssh -D 1080 user@server
    Config:  Set browser proxy to SOCKS5 localhost:1080
             All browsing now goes through SSH server

.. code-block:: bash

    # Command line usage
    ssh -D 1080 -N -f user@server

    # -D 1080: Dynamic forwarding on port 1080
    # -N: No remote command (just forwarding)
    # -f: Background after authentication

    # Use with curl
    curl --socks5 localhost:1080 http://internal-site.local

Jump Hosts (ProxyJump)
----------------------

Jump hosts (also called bastion hosts or gateway servers) are hardened machines
that provide the only entry point into a private network. Instead of exposing
internal servers directly to the internet, organizations route all SSH access
through a jump host that can be heavily monitored and secured. SSH's ``ProxyJump``
(``-J``) option makes this seamless—you specify the jump host, and SSH automatically
chains the connections, authenticating to each hop. The connection to the final
destination is end-to-end encrypted; the jump host only sees encrypted traffic
passing through. You can chain multiple jump hosts for deeply segmented networks.
This pattern is fundamental to secure infrastructure access in cloud environments
where production servers should never have public IP addresses.

::

    ┌──────────┐      ┌──────────────┐      ┌──────────────┐
    │  Your    │ SSH  │   Bastion    │ SSH  │   Internal   │
    │  Machine │═════►│   (jump)     │═════►│   Server     │
    │          │      │              │      │              │
    └──────────┘      └──────────────┘      └──────────────┘

    Command: ssh -J user@bastion user@internal-server

    Or in ~/.ssh/config:
    Host internal-server
        HostName 10.0.0.50
        User admin
        ProxyJump user@bastion.example.com

.. code-block:: python

    # Jump host with Paramiko
    from paramiko.client import SSHClient

    # Connect to bastion first
    bastion = SSHClient()
    bastion.load_system_host_keys()
    bastion.connect("bastion.example.com", username="user", key_filename="mykey")

    # Get transport and open channel to internal host
    bastion_transport = bastion.get_transport()
    dest_addr = ("internal-server.local", 22)
    local_addr = ("127.0.0.1", 0)
    channel = bastion_transport.open_channel("direct-tcpip", dest_addr, local_addr)

    # Connect to internal server through the channel
    internal = SSHClient()
    internal.load_system_host_keys()
    internal.connect(
        "internal-server.local",
        username="admin",
        key_filename="mykey",
        sock=channel  # Use bastion channel as socket
    )

    # Execute command on internal server
    stdin, stdout, stderr = internal.exec_command("hostname")
    print(stdout.read().decode())

    internal.close()
    bastion.close()

SSH Config File
---------------

The SSH config file (``~/.ssh/config``) eliminates repetitive command-line options
by defining per-host settings. Instead of typing ``ssh -i ~/.ssh/mykey -p 2222
user@long.hostname.example.com``, you define a host alias and simply type
``ssh myserver``. The config file supports wildcards, allowing you to set defaults
for groups of hosts (all ``*.internal`` hosts use a specific jump server). You can
also define automatic port forwarding, so connecting to a host automatically sets
up your database tunnels. For teams, a shared config file ensures everyone uses
consistent, secure settings. The config is processed top-to-bottom with first
match winning, so put specific hosts before wildcards.

.. code-block:: text

    # ~/.ssh/config

    # Default settings for all hosts
    Host *
        ServerAliveInterval 60
        ServerAliveCountMax 3
        AddKeysToAgent yes

    # Simple host alias
    Host myserver
        HostName server.example.com
        User admin
        Port 2222
        IdentityFile ~/.ssh/mykey

    # Jump host configuration
    Host bastion
        HostName bastion.example.com
        User jumpuser
        IdentityFile ~/.ssh/bastion_key

    Host internal-*
        ProxyJump bastion
        User admin
        IdentityFile ~/.ssh/internal_key

    Host internal-db
        HostName 10.0.0.50

    Host internal-web
        HostName 10.0.0.51

    # Local port forwarding on connect
    Host db-tunnel
        HostName bastion.example.com
        User admin
        LocalForward 5432 db.internal:5432
        LocalForward 6379 redis.internal:6379

SSH Agent Forwarding
--------------------

SSH agent forwarding lets you use your local private keys on remote servers without
copying the keys there. When you SSH to a server with agent forwarding enabled
(``-A``), the remote server can request signatures from your local ssh-agent for
subsequent SSH connections. This is essential for workflows like cloning private
git repositories from a server or hopping through multiple machines. However, agent
forwarding has security implications: anyone with root access on the remote server
can use your forwarded agent to authenticate as you to other systems while you're
connected. For sensitive environments, consider ``ProxyJump`` instead, which keeps
your keys local, or use per-host deploy keys.

.. code-block:: bash

    # Enable agent forwarding
    ssh -A user@server

    # On server, your local keys are available
    git clone git@github.com:user/repo.git  # Uses forwarded key

.. code-block:: python

    # Agent forwarding with Paramiko
    from paramiko.client import SSHClient
    from paramiko.agent import Agent

    # Get keys from local SSH agent
    agent = Agent()
    agent_keys = agent.get_keys()

    with SSHClient() as ssh:
        ssh.load_system_host_keys()
        # Connect using agent key
        ssh.connect("server.example.com", username="user", pkey=agent_keys[0])

        # Enable agent forwarding for this session
        transport = ssh.get_transport()
        paramiko.agent.AgentRequestHandler(transport.open_session())

Keepalive and Connection Stability
----------------------------------

SSH connections can silently die due to network issues, NAT gateway timeouts, or
stateful firewalls that drop idle connections. Without keepalives, you won't know
the connection is dead until you try to use it—resulting in hung terminals or
failed operations. SSH provides two keepalive mechanisms: ``TCPKeepAlive`` uses
TCP-level keepalive packets (can be blocked by some firewalls), while
``ServerAliveInterval`` sends SSH-protocol messages through the encrypted channel
(more reliable). ``ServerAliveCountMax`` determines how many missed responses
trigger disconnect. For reliable long-running connections—tunnels, interactive
sessions, or automation—configure both client and server keepalives. A 30-60
second interval works well for most NAT environments.

.. code-block:: python

    from paramiko.client import SSHClient

    with SSHClient() as ssh:
        ssh.load_system_host_keys()
        ssh.connect("server.example.com", username="user", key_filename="mykey")

        # Configure keepalive
        transport = ssh.get_transport()
        transport.set_keepalive(30)  # Send keepalive every 30 seconds

        # Long-running operations...

.. code-block:: text

    # In ~/.ssh/config
    Host *
        ServerAliveInterval 30
        ServerAliveCountMax 3
        TCPKeepAlive yes

Common SSH Commands Reference
-----------------------------

A quick reference for essential SSH commands covering connections, tunneling, key
management, and file transfer. These commands form the foundation of secure remote
administration and are worth committing to memory. The verbose flags (``-v`` to
``-vvv``) are invaluable for debugging connection issues, showing the authentication
methods tried, key exchanges, and where failures occur.

.. code-block:: bash

    # Basic connection
    ssh user@host
    ssh -p 2222 user@host              # Custom port
    ssh -i ~/.ssh/mykey user@host      # Specific key

    # Tunneling
    ssh -L 8080:localhost:80 user@host # Local forward
    ssh -R 9000:localhost:3000 user@host # Remote forward
    ssh -D 1080 user@host              # SOCKS proxy

    # Jump hosts
    ssh -J jump@bastion user@internal  # ProxyJump
    ssh -o ProxyCommand="ssh -W %h:%p jump@bastion" user@internal

    # Background tunnels
    ssh -N -f -L 5432:db:5432 user@host  # -N no command, -f background

    # Key management
    ssh-keygen -t ed25519 -C "comment"   # Generate key (ed25519 recommended)
    ssh-keygen -t rsa -b 4096            # RSA 4096-bit
    ssh-copy-id -i ~/.ssh/mykey user@host # Copy public key to server
    ssh-add ~/.ssh/mykey                 # Add key to agent

    # Debugging
    ssh -v user@host                     # Verbose
    ssh -vvv user@host                   # Very verbose

    # File transfer
    scp local.txt user@host:/path/       # Copy to remote
    scp user@host:/path/file.txt .       # Copy from remote
    scp -r dir/ user@host:/path/         # Recursive copy
    rsync -avz -e ssh dir/ user@host:/path/  # Efficient sync
