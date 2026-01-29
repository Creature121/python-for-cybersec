from scapy.layers.dns import DNS
from scapy.layers.inet import IP
from scapy.sendrecv import sniff

from scapy.all import *  # noqa: F403
from base64 import b64decode
from pandas import Series
from scipy.stats import entropy


def calcEntropy(data):
    s_data = Series(data)
    counts = s_data.value_counts()
    return entropy(counts)


threshold = 100


def testData(data):
    if calcEntropy(data) > threshold:
        return "encrypted"
    try:
        decoded = b64decode(data)
        return decoded
    except Exception as _:
        return False


def processPacket(packet):
    if packet.haslayer(IP):
        src = packet[IP].src
        dst = packet[IP].dst
    else:
        return

    if packet.haslayer(DNS):
        hostname = packet[DNS].qd.qname.decode("utf-8")
        d = hostname.split(".")
        for v in d:
            result = testData(v)
            if result == "encrypted":
                print(f"Potentially encrypted data in DNS packet {src}->{dst}")
            elif result:
                print(f"Extracted data {result} from DNS packet {src}->{dst}")


sniff(prn=processPacket)
