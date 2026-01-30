from scapy.packet import Packet
from scapy.layers.inet import ICMP
from scapy.sendrecv import sniff

from scapy.all import *  # noqa: F403


def printData(packet: Packet):
    data = chr(packet[ICMP].code)
    print(data, end="", flush=True)


sniff(filter="icmp", prn=printData)
