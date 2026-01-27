from scapy.all import sr, IP, TCP  # ty:ignore[unresolved-import]

import ipaddress


ports = [25, 80, 53, 443, 445, 8080, 8443]

# The weird formating of the argument in sr() is actually Scapy overloading the division (/) operator, to allow a sort of "layering" style to the various parts of a packet.


def SynScan(host):
    answered, unanswered = sr(
        IP(dst=host) / TCP(sport=33333, dport=ports, flags="S"), timeout=2, verbose=0
    )

    (open_ports, closed_ports, filtered_ports) = (
        [],
        [],
        [sent_packet[TCP].dport for sent_packet in unanswered],
    )

    for sent_packet, received_packet in answered:
        # print(received_packet[TCP].flags)
        if sent_packet[TCP].dport == received_packet[TCP].sport:
            if received_packet[TCP].flags == "SA":
                open_ports.append(sent_packet[TCP].dport)
            if "R" in received_packet[TCP].flags:
                closed_ports.append(sent_packet[TCP].dport)

    print()
    print(f"{host}:")
    for word, port_list in zip(
        ("Open", "Closed", "Filtered"), (open_ports, closed_ports, filtered_ports)
    ):
        print(f"{word} ports: {port_list}")
    print()


host = input("Enter IP Address: ")
try:
    ipaddress.ip_address(host)
except:  # noqa: E722
    print("Invalid IP Adress")
    exit(-1)

SynScan(host)
