# from scapy.all import *
from scapy.all import Packet, Raw, IP, TCP, rdpcap  # ty:ignore[unresolved-import]
from base64 import b64decode
import re


def ExtractFTP(packet):
    payload = packet[Raw].load.decode("utf-8").rstrip()

    if payload[:4] == "USER":
        print(f"{packet[IP].dst} FTP Username: {payload[5:]}")
    elif payload[:4] == "PASS":
        print(f"{packet[IP].dst} FTP Password: {payload[5:]}")


email_regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
unmatched = []


def ExtractSMTP(packet):
    payload = packet[Raw].load
    try:
        decoded = b64decode(payload)
        decoded = decoded.decode("utf-8")
        connection_data = [packet[IP].src, packet[TCP].sport]

        if re.search(email_regex, decoded):
            print(f"{packet[IP].dst} SMTP Username: {decoded}")
            unmatched.append([packet[IP].src, packet[TCP].sport])
        elif connection_data in unmatched:
            print(f"{packet[IP].dst} SMTP Password: {decoded}")
            unmatched.remove(connection_data)
    except Exception as e:
        # print(f"Error in ExtractSMTP()\n{e}")
        return


awaiting_login = []
awaiting_password = []


def ExtractTelnet(packet):
    try:
        payload = packet[Raw].load.decode("utf-8").rstrip()
    except Exception as e:
        # print(f"Failed to extract payload.\n{e}")
        return

    if packet[TCP].sport == 23:
        connection_data = [packet[IP].src, packet[TCP].sport]
        if payload[:5] == "login":
            awaiting_login.append(connection_data)
            return
        elif payload[:8] == "Password":
            awaiting_password.append(connection_data)
            return
    else:
        connection_data = [packet[IP].dst, packet[TCP].dport]
        if connection_data in awaiting_login:
            print(f"{packet[IP].dst} Telnet Username: {payload}")
            awaiting_login.remove(connection_data)
        elif connection_data in awaiting_password:
            print(f"{packet[IP].dst} Telnet Password: {payload}")
            awaiting_password.remove(connection_data)


packets = rdpcap("merged.pcap")

for packet in packets:
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        if packet[TCP].dport == 21:
            ExtractFTP(packet)
        elif packet[TCP].dport == 25:
            ExtractSMTP(packet)
        elif packet[TCP].sport == 23 or packet.dport == 23:
            ExtractTelnet(packet)
