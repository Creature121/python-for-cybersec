from scapy.packet import Packet
from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import send

from scapy.all import *  # noqa: F403


def transmit(message, host):
    for m in message:
        packet: Packet = IP(dst=host) / ICMP(code=ord(m))
        send(packet)


host = ""
message = "Hello"
transmit(message, host)
