.. meta::
    :description lang=en: Python packet sniffing and raw socket programming tutorial for capturing and parsing IP, TCP, UDP, ARP packets, network analysis, and Linux kernel crypto API
    :keywords: Python, socket, raw socket, packet sniffer, IP header, TCP header, ARP, network analysis, ctypes, struct, Wireshark, tcpdump, AF_ALG, kernel crypto, scapy

================
Packet Sniffing
================

.. contents:: Table of Contents
    :backlinks: none

Raw sockets provide direct access to network packets at the IP layer and below,
bypassing the normal TCP/UDP protocol stack. This low-level access is essential for
building network analysis tools, intrusion detection systems, custom protocol
implementations, and security research tools. While libraries like Wireshark and
tcpdump are commonly used for packet capture, understanding how to parse packets
in Python gives you the flexibility to build custom analysis tools tailored to
your specific needs.

This section covers capturing and parsing network packets using Python's raw socket
interface, the ``ctypes`` module for defining C-compatible data structures, and the
``struct`` module for binary data parsing. You'll learn to decode IP headers to
extract source and destination addresses, parse TCP headers to analyze connection
states and flags, capture ARP packets to monitor address resolution, and use the
Linux kernel's AF_ALG interface for hardware-accelerated cryptography. These
techniques form the foundation for building tools like network monitors, protocol
analyzers, and security scanners.

.. warning::

    Raw socket operations typically require root/administrator privileges on most
    operating systems. Use these techniques responsibly and only on networks you
    own or have explicit permission to analyze. Unauthorized packet sniffing may
    violate laws and regulations in your jurisdiction.

Sniffer IP Packets
------------------

Capturing IP packets requires creating a raw socket with ``SOCK_RAW`` and specifying
the protocol to capture (e.g., ``IPPROTO_ICMP`` for ICMP packets). The IP header is
a 20-byte structure (without options) containing version, header length, type of
service, total length, identification, flags, fragment offset, TTL, protocol, checksum,
and source/destination addresses. Using ``ctypes.Structure``, we can define a Python
class that maps directly to this binary layout for easy field access.

.. code-block:: python

    from ctypes import Structure, c_ubyte, c_uint8, c_uint16, c_uint32
    import socket
    import struct

    # IP protocol numbers
    PROTO_MAP = {
        1: "ICMP",
        2: "IGMP",
        6: "TCP",
        17: "UDP",
        27: "RDP"
    }

    class IP(Structure):
        """IP header structure (20 bytes)."""
        _fields_ = [
            ("ip_hl", c_ubyte, 4),   # Header length
            ("ip_v", c_ubyte, 4),    # Version
            ("ip_tos", c_uint8),     # Type of service
            ("ip_len", c_uint16),    # Total length
            ("ip_id", c_uint16),     # Identification
            ("ip_off", c_uint16),    # Fragment offset
            ("ip_ttl", c_uint8),     # Time to live
            ("ip_p", c_uint8),       # Protocol
            ("ip_sum", c_uint16),    # Checksum
            ("ip_src", c_uint32),    # Source address
            ("ip_dst", c_uint32),    # Destination address
        ]

        def __new__(cls, buf=None):
            return cls.from_buffer_copy(buf)

        def __init__(self, buf=None):
            src = struct.pack("<L", self.ip_src)
            self.src = socket.inet_ntoa(src)
            dst = struct.pack("<L", self.ip_dst)
            self.dst = socket.inet_ntoa(dst)
            self.proto = PROTO_MAP.get(self.ip_p, f"Unknown({self.ip_p})")

    # Create raw socket for ICMP
    host = '0.0.0.0'
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    s.bind((host, 0))

    print("Sniffer start... (Ctrl+C to stop)")
    try:
        while True:
            buf = s.recvfrom(65535)[0]
            ip_header = IP(buf[:20])
            print(f'{ip_header.proto}: {ip_header.src} -> {ip_header.dst}')
    except KeyboardInterrupt:
        s.close()

Output:

.. code-block:: console

    $ sudo python sniffer.py
    Sniffer start...
    ICMP: 127.0.0.1 -> 127.0.0.1
    ICMP: 127.0.0.1 -> 127.0.0.1

Sniffer TCP Packets
-------------------

Parse TCP headers to extract port numbers, sequence numbers, and flags.

.. code-block:: python

    import socket
    import platform
    from struct import unpack
    from contextlib import contextmanager

    if platform.system() != "Linux":
        print("This example requires Linux")
        exit(1)

    @contextmanager
    def create_socket():
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        try:
            yield s
        finally:
            s.close()

    def parse_tcp_packet(pkt):
        # IP header (first 20 bytes, variable length)
        iphdr = unpack('!BBHHHBBH4s4s', pkt[0:20])
        iplen = (iphdr[0] & 0xf) * 4

        # TCP header (next 20 bytes minimum)
        tcphdr = unpack('!HHLLBBHHH', pkt[iplen:iplen+20])

        return {
            'src_port': tcphdr[0],
            'dst_port': tcphdr[1],
            'seq': tcphdr[2],
            'ack': tcphdr[3],
            'data_offset': tcphdr[4] >> 4,
            'flags': {
                'FIN': tcphdr[5] & 0x01,
                'SYN': tcphdr[5] & 0x02,
                'RST': tcphdr[5] & 0x04,
                'PSH': tcphdr[5] & 0x08,
                'ACK': tcphdr[5] & 0x10,
                'URG': tcphdr[5] & 0x20,
            },
            'window': tcphdr[6],
            'checksum': tcphdr[7],
        }

    try:
        with create_socket() as s:
            print("TCP Sniffer started...")
            while True:
                pkt, addr = s.recvfrom(65535)
                tcp = parse_tcp_packet(pkt)

                # Skip packets without data
                iplen = (pkt[0] & 0xf) * 4
                tcplen = tcp['data_offset'] * 4
                data = pkt[iplen + tcplen:]
                if not data:
                    continue

                flags = [k for k, v in tcp['flags'].items() if v]
                print(f"Port {tcp['src_port']} -> {tcp['dst_port']} "
                      f"[{','.join(flags)}] Seq={tcp['seq']}")
                print(f"Data: {data[:50]}...")
    except KeyboardInterrupt:
        pass

Sniffer ARP Packets
-------------------

Capture ARP (Address Resolution Protocol) packets to see MAC-to-IP mappings.

.. code-block:: python

    import socket
    import struct
    import binascii

    # Create raw socket for all packets
    rawSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW,
                              socket.htons(0x0003))

    print("ARP Sniffer started...")
    while True:
        packet = rawSocket.recvfrom(2048)

        # Ethernet header (14 bytes)
        ethhdr = packet[0][0:14]
        eth = struct.unpack("!6s6s2s", ethhdr)

        # Check if ARP packet (0x0806)
        if eth[2] != b'\x08\x06':
            continue

        # ARP header (28 bytes)
        arphdr = packet[0][14:42]
        arp = struct.unpack("2s2s1s1s2s6s4s6s4s", arphdr)

        print("=" * 50)
        print("ETHERNET FRAME")
        print(f"  Dest MAC:   {binascii.hexlify(eth[0]).decode()}")
        print(f"  Source MAC: {binascii.hexlify(eth[1]).decode()}")
        print("ARP HEADER")
        print(f"  Hardware:   {binascii.hexlify(arp[0]).decode()}")
        print(f"  Protocol:   {binascii.hexlify(arp[1]).decode()}")
        print(f"  Opcode:     {binascii.hexlify(arp[4]).decode()} "
              f"({'Request' if arp[4] == b'\\x00\\x01' else 'Reply'})")
        print(f"  Sender MAC: {binascii.hexlify(arp[5]).decode()}")
        print(f"  Sender IP:  {socket.inet_ntoa(arp[6])}")
        print(f"  Target MAC: {binascii.hexlify(arp[7]).decode()}")
        print(f"  Target IP:  {socket.inet_ntoa(arp[8])}")

Parse Packet with struct
------------------------

Using ``struct`` module for flexible packet parsing.

.. code-block:: python

    import struct
    import socket

    def parse_ip_header(data):
        """Parse IP header from raw bytes."""
        # ! = network byte order (big-endian)
        # B = unsigned char, H = unsigned short, 4s = 4-byte string
        fields = struct.unpack('!BBHHHBBH4s4s', data[:20])

        return {
            'version': fields[0] >> 4,
            'ihl': fields[0] & 0x0F,
            'tos': fields[1],
            'total_length': fields[2],
            'identification': fields[3],
            'flags': fields[4] >> 13,
            'fragment_offset': fields[4] & 0x1FFF,
            'ttl': fields[5],
            'protocol': fields[6],
            'checksum': fields[7],
            'src_ip': socket.inet_ntoa(fields[8]),
            'dst_ip': socket.inet_ntoa(fields[9]),
        }

    def parse_udp_header(data):
        """Parse UDP header from raw bytes."""
        fields = struct.unpack('!HHHH', data[:8])
        return {
            'src_port': fields[0],
            'dst_port': fields[1],
            'length': fields[2],
            'checksum': fields[3],
        }

    # Example usage with captured packet
    # ip_data = ... (raw IP packet bytes)
    # ip = parse_ip_header(ip_data)
    # if ip['protocol'] == 17:  # UDP
    #     udp = parse_udp_header(ip_data[ip['ihl']*4:])

Linux Kernel Crypto API (AF_ALG)
--------------------------------

Use Linux kernel's cryptographic API through sockets for hardware-accelerated
encryption. Requires Linux 2.6.38+ and Python 3.6+.

.. code-block:: python

    import socket
    import hashlib
    import contextlib

    @contextlib.contextmanager
    def create_alg(typ, name):
        s = socket.socket(socket.AF_ALG, socket.SOCK_SEQPACKET, 0)
        try:
            s.bind((typ, name))
            yield s
        finally:
            s.close()

    # SHA-256 hash using kernel crypto
    msg = b'Python is awesome!'

    with create_alg('hash', 'sha256') as algo:
        op, _ = algo.accept()
        with op:
            op.sendall(msg)
            digest = op.recv(512)
            print(f"AF_ALG SHA256: {digest.hex()}")

            # Verify against hashlib
            expected = hashlib.sha256(msg).digest()
            assert digest == expected

AES-CBC Encryption via AF_ALG
-----------------------------

.. code-block:: python

    import socket
    import os

    BS = 16  # Block size
    pad = lambda s: s + (BS - len(s) % BS) * bytes([BS - len(s) % BS])
    unpad = lambda s: s[:-s[-1]]

    def aes_cbc_encrypt(plaintext, key, iv):
        with socket.socket(socket.AF_ALG, socket.SOCK_SEQPACKET, 0) as algo:
            algo.bind(('skcipher', 'cbc(aes)'))
            algo.setsockopt(socket.SOL_ALG, socket.ALG_SET_KEY, key)
            op, _ = algo.accept()
            with op:
                plaintext = pad(plaintext)
                op.sendmsg_afalg([plaintext],
                                op=socket.ALG_OP_ENCRYPT,
                                iv=iv)
                return op.recv(len(plaintext))

    def aes_cbc_decrypt(ciphertext, key, iv):
        with socket.socket(socket.AF_ALG, socket.SOCK_SEQPACKET, 0) as algo:
            algo.bind(('skcipher', 'cbc(aes)'))
            algo.setsockopt(socket.SOL_ALG, socket.ALG_SET_KEY, key)
            op, _ = algo.accept()
            with op:
                op.sendmsg_afalg([ciphertext],
                                op=socket.ALG_OP_DECRYPT,
                                iv=iv)
                return unpad(op.recv(len(ciphertext)))

    # Example
    key = os.urandom(32)  # AES-256
    iv = os.urandom(16)
    plaintext = b"Secret message!"

    ciphertext = aes_cbc_encrypt(plaintext, key, iv)
    decrypted = aes_cbc_decrypt(ciphertext, key, iv)

    print(f"Ciphertext: {ciphertext.hex()}")
    print(f"Decrypted: {decrypted}")

Useful Tools for Packet Analysis
--------------------------------

While raw sockets are educational, consider these tools for production use:

.. code-block:: python

    # Scapy - powerful packet manipulation library
    # pip install scapy
    from scapy.all import sniff, IP, TCP

    def packet_callback(pkt):
        if IP in pkt and TCP in pkt:
            print(f"{pkt[IP].src}:{pkt[TCP].sport} -> "
                  f"{pkt[IP].dst}:{pkt[TCP].dport}")

    # Sniff 10 TCP packets
    sniff(filter="tcp", prn=packet_callback, count=10)

    # dpkt - fast packet parsing
    # pip install dpkt
    import dpkt

    with open('capture.pcap', 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)
            if isinstance(eth.data, dpkt.ip.IP):
                ip = eth.data
                print(f"{dpkt.utils.inet_to_str(ip.src)} -> "
                      f"{dpkt.utils.inet_to_str(ip.dst)}")
