import dns
import dns.resolver
import socket

domains = {}
sub_domains = "dns_search.txt"

resolver = dns.resolver.Resolver()
resolver.nameservers = ["127.0.0.1"]
resolver.port = 8053

domain = "example.com"
add_numbers = False


def ReversDNS(ip):
    # print(f"Triggered ReverseDNS request for {ip}...")
    try:
        result = socket.gethostbyaddr(ip)
        return [result[0]] + result[1]
    except socket.herror:
        return []


def DNSRequest(domain):
    # print(f"Triggered DNS request for {domain}...")
    # global domains # Added this in myself, otherwise the code wouldn't work...
    ips = []
    try:
        result = resolver.resolve(domain)
        if result:
            # print(result)
            addresses = [address.to_text() for address in result]
            if domain in domains:
                domains[domain] = list(set(domains[domain] + addresses))
            else:
                domains[domain] = addresses
            for address in addresses:
                reverse_domain = ReversDNS(address)
                for domain in reverse_domain:
                    if domain not in domains:
                        domains[domain] = [address]
                        DNSRequest(domain)
                    else:
                        domains[domain] = [address]
    except (
        dns.resolver.NXDOMAIN,
        dns.exception.Timeout,
        dns.resolver.NoAnswer,
    ):  # Added dns.resolver.NoAnswer to deal with error
        return []
    return ips


def HostSearch(domain, dictionary, add_numbers):
    successes = []  # unused variable??
    for word in dictionary:
        new_domain = f"{word}.{domain}"
        DNSRequest(new_domain)
        if add_numbers:
            for i in range(0, 10):
                alt_domain = f"{word}{i}.{domain}"
                DNSRequest(alt_domain)


dictionary = []
with open(sub_domains, "r") as f:
    dictionary = f.read().splitlines()
HostSearch(domain, dictionary, add_numbers)
for domain in domains:
    print(f"{domain}: {domains[domain]}")

# Created dns_search.txt
