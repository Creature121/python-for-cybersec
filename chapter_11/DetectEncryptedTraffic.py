from scapy.packet import Packet, Raw
from scapy.sendrecv import sniff

from scapy.all import *  # noqa: F403
from pandas import Series
from scipy.stats import entropy

def calcEntropy(data):
    b = bytearray(data)
    s = Series(b)
    counts = s.value_counts()
    return entropy(counts)

entropy_threshold = 2.5
def processPayloads(packet: Packet):
    if not packet.haslayer(Raw):
        return
    load = packet[Raw].load
    e = calcEntropy(load)
    if e >= entropy_threshold and len(load) % 16 == 0:
        print(f"Potentially encrypted data detected with entropy {e:.3f}")
        print(f"\t{load.hex()}")
    return

sniff(offline="EncryptedChannel.pcapng", prn=processPayloads)