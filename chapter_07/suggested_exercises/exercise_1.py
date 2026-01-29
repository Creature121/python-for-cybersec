from scapy.all import Raw, IP, TCP, rdpcap, UDP  # ty:ignore[unresolved-import]
from base64 import b64decode
import re


def ExtractFTP(packet):
    payload = packet[Raw].load.decode("utf-8").rstrip()

    if payload[:4] == "USER":
        print(f"{packet[IP].dst} FTP Username: {payload[5:]}")
    elif payload[:4] == "PASS":
        print(f"{packet[IP].dst} FTP Password: {payload[5:]}")


def ExtractNetBiosDetails(packet):
    payload = bytes(packet[UDP].payload)
    # print(payload)
    # print(payload[0])

    msg_type = payload[0]
    flags = payload[1]
    datagram_id = payload[2:4]
    src_ip, dst_ip = packet[IP].src, packet[IP].dst
    datagram_source_name = payload[14:48]
    datagram_destination_name = payload[48:88]

    print(f"NBD from  ({src_ip}) -> ({dst_ip})")
    print(f"Datagram Source Name: {datagram_source_name}")
    print(f"Datagram Destination Name: {datagram_destination_name}")
    print(f"\tID: 0x{datagram_id.hex()}")
    print(f"\tType: 0x{msg_type:02x}")
    print(f"\tFlags: 0x{flags:02x}")
    # print(f"\tFlags: 0x{flags:02x}")


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


packets = rdpcap("../merged.pcap")

for packet in packets:
    if packet.haslayer(Raw):
        if packet.haslayer(TCP):
            if packet[TCP].dport == 21:
                ExtractFTP(packet)
            elif packet[TCP].dport == 25:
                ExtractSMTP(packet)
            elif packet[TCP].sport == 23 or packet.dport == 23:
                ExtractTelnet(packet)
        elif packet.haslayer(UDP):
            if 138 in (packet[UDP].sport, packet[UDP].dport):
                ExtractNetBiosDetails(packet)
