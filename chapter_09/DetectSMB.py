from scapy.layers.smb2 import SMB2_Header
from scapy.packet import Packet, Raw
from scapy.sendrecv import sniff

from scapy.all import *  # noqa: F403
import re
import struct


def processPacket(packet: Packet):
    if not packet.haslayer(SMB2_Header):
        # print("Triggered")
        return
    # else:
    # print("Not Triggered")

    cmd = packet[SMB2_Header].Command

    if cmd in [1280]:
        data = packet[Raw].load.decode("utf-16")
        matches = re.findall("[ -~]*[.][ -~]*", data)
        if matches:
            print(f"File operation detected: {matches}")
    elif cmd == 256:
        load = packet[Raw].load
        try:
            index = load.index(bytes("NTLMSSP", "utf-8"))
        except Exception as e:
            print(f"(Error: {e})")
            return

        if index > -1 and load[index + 8] == 3:
            name_len = struct.unpack("<h", load[index + 36 : index + 38])[0]
            offset = index + struct.unpack("<hh", load[index + 40 : index + 44])[0]
            user_name = load[offset : offset + name_len].decode("utf-16")
            print(f"Account Access Attempt: {user_name}")
    # else:
    # print("nope")


sniff(offline="SMB.pcapng", prn=processPacket)
