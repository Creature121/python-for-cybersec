from scapy.layers.dhcp import IP
from scapy.sendrecv import sniff
from scapy.layers.http import HTTPRequest

from scapy.all import *  # noqa: F403
from scapy.layers.http import *  # noqa: F403

decoy_domains = ".fake.com"


def processHTTP(packet):
    if packet.haslayer(HTTPRequest):
        if packet[HTTPRequest].Cookie:
            host = packet[HTTPRequest].Host.decode()
            decoy = [host.endswith(d) for d in decoy_domains]
            if True in decoy:
                print(f"Request to decoy domain {host} from {packet[IP].src}")


sniff(offline="decoyCookie.pcap", prn=processHTTP)
