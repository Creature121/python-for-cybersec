# from icecream import ic
from scapy.layers.smb2 import SMB2_Header
from scapy.packet import Packet, Raw
from scapy.sendrecv import sniff

from scapy.all import *  # noqa: F403
import re
import struct


def processPacket(packet: Packet):
    if not packet.haslayer(SMB2_Header):
        return

    # cmd = packet[SMB2_Header].Command

    # ic(f"{list(packet[SMB2_Header].getfieldval('Command').to_bytes(2, byteorder='little'))}")

    raw_cmd = packet[SMB2_Header].getfieldval("Command")
    cmd = list(raw_cmd.to_bytes(2, byteorder="little"))[1]

    if cmd == 5:
        data = packet[Raw].load.decode("utf-16")
        matches = re.findall("[ -~]*[.][ -~]*", data)
        if matches:
            print(f"Create File operation detected: {matches}")
    elif cmd == 9:
        data = packet[SMB2_Header].payload.load
        if text := data[45:]:
            print("Write Request Detected:")
            print(f"\tContent:\n\t\t{text}")
        else:
            print("Write Response Detected.")
    elif cmd == 1:
        load = packet[Raw].load
        try:
            index = load.index(bytes("NTLMSSP", "utf-8"))
        except Exception as e:
            print(f"(Error: NTLMSSP not found?)\n\t({e})")
            return

        if index > -1 and load[index + 8] == 3:
            name_len = struct.unpack("<h", load[index + 36 : index + 38])[0]
            offset = index + struct.unpack("<hh", load[index + 40 : index + 44])[0]
            user_name = load[offset : offset + name_len].decode("utf-16")
            print(f"Account Access Attempt: {user_name}")


sniff(offline="../SMB.pcapng", prn=processPacket)
