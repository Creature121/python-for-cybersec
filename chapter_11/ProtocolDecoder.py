from scapy.packet import Packet, Raw
from scapy.layers.http import HTTPRequest, HTTPResponse
from scapy.sendrecv import sniff

from scapy.all import *  # noqa: F403
from scapy.layers.http import *  # noqa: F403
from base64 import b64decode
import re

b64_regex = b"[A-za-z0-9+/=]+"


def extractData(data):
    data = data.rstrip()
    matches = re.findall(b64_regex, data)
    for match in matches:
        if len(match) == 0:
            continue
        try:
            if not len(match) % 4 == 0:
                pad_number = (4 - len(match) % 4) % 4
                match += b"=" * pad_number
            decoded = b64decode(match).decode("utf-8")
            if len(decoded) > 5 and decoded.isprintable():
                print(f"Decoded: {decoded}")
        except Exception as _:
            continue


def extractHTTP(packet: Packet):
    fields = None
    if packet.haslayer(HTTPRequest):
        fields = packet[HTTPRequest].fields
    else:
        fields = packet[HTTPResponse].fields

    for f in fields:
        data = fields[f]
        if isinstance(data, str):
            extractData(data)
        elif isinstance(data, dict):
            for d in data:
                extractData(data[d])
        elif isinstance(data, list) or isinstance(data, tuple):
            for d in data:
                extractData(d)


def extractRaw(packet: Packet):
    extractData(packet[Raw].load)


def analysePackets(packet: Packet):
    if packet.haslayer(HTTPRequest) or packet.haslayer(HTTPResponse):
        packet.show()
        extractHTTP(packet)
    elif packet.haslayer(Raw):
        extractRaw(packet)


sniff(prn=analysePackets)
