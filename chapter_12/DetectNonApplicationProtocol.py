from scapy.packet import Packet
from scapy.layers.inet import ICMP
from scapy.sendrecv import sniff

from scapy.all import *  # noqa: F403

# Based on
# https://www.iana.org/assignments/icmp-parameters/icmp-parameters.xhtml
# (according to the author)

type_code = {
    0: [0],
    3: [x for x in range(16)],
    5: [x for x in range(4)],
    8: [0],
    9: [0, 16],
    10: [0],
    11: [0, 1],
    12: [0, 1, 2],
    13: [0],
    14: [0],
    40: [x for x in range(6)],
    41: [],
    42: [0],
    43: [x for x in range(5)],
    253: [],
    254: [],
}


def testICMP(packet: Packet):
    p_type = packet[ICMP].type
    p_code = packet[ICMP].code

    if p_type in type_code:
        if p_code not in type_code[p_type]:
            print(f"Anomalous code detected {p_type}/{chr(p_type)}")  # Not p_code?
    else:
        print(f"Anomalous type detected {p_type}/{chr(p_type)}")


def processPacket(packet: Packet):
    if packet.haslayer(ICMP):
        testICMP(packet)


sniff(prn=processPacket)
