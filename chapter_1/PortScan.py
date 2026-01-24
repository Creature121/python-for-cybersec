from scapy.all import sr, IP, TCP, UDP, DNS, DNSQR

import ipaddress


ports = [25, 80, 53, 443, 445, 8080, 8443]

# The weird formating of the argument in sr() is actually Scapy overloading the division (/) operator, to allow a sort of "layering" style to the various parts of a packet.


def SynScan(host):
    answered, unanswered = sr(
        IP(dst=host) / TCP(sport=33333, dport=ports, flags="S"), timeout=2, verbose=0
    )

    print(f"Open ports at {host}:")
    for sent_packet, received_packet in answered:
        if (
            sent_packet[TCP].dport == received_packet["TCP"].sport
            and received_packet["TCP"].flags == "SA"
        ):
            print(sent_packet[TCP].dport)


def DNSScan(host):
    answered, unanswered = sr(
        IP(dst=host) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname="google.com")),
        timeout=2,
        verbose=0,
    )
    if answered or answered[UDP]:  # Also example of method overloading?
        print(f"DNS Server at {host}")


host = input("Enter IP Address: ")
try:
    ipaddress.ip_address(host)
except:  # noqa: E722
    print("Invalid IP Adress")
    exit(-1)

SynScan(host)
DNSScan(host)

# Looks like 8.8.8.8 isn't a DNS server? (Output isn't indicating as such...probably a code error.)
