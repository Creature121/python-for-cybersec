import dns
import dns.resolver
import socket
from concurrent.futures import (
    ThreadPoolExecutor,
)  # Added a ThreadPoolExecutor to speed up everything

domains = {}
sub_domains = "../dns_search.txt"
executor = ThreadPoolExecutor(max_workers=8 * 4)

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
    ips = []
    try:
        result = resolver.resolve(domain)
        # print(result)
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
                        executor.submit(DNSRequest, domain)
                        # DNSRequest(domain)
                    else:
                        domains[domain] = [address]
    except (
        dns.resolver.NXDOMAIN,
        dns.exception.Timeout,  # ty:ignore[possibly-missing-attribute]
        dns.resolver.NoAnswer,
    ):  # Added dns.resolver.NoAnswer to deal with error
        return []
    return ips


def HostSearch(domain, dictionary, add_numbers):
    successes = []  # unused variable??  # noqa: F841
    for word in dictionary:
        new_domain = f"{word}.{domain}"
        executor.submit(DNSRequest, new_domain)
        # DNSRequest(new_domain)
        if add_numbers:
            for i in range(0, 10):
                alt_domain = f"{word}{i}.{domain}"
                executor.submit(DNSRequest, alt_domain)
                # DNSRequest(alt_domain)


dictionary = []
with open(sub_domains, "r") as f:
    dictionary = f.read().splitlines()
HostSearch(domain, dictionary, add_numbers)
executor.shutdown()
# for domain in domains:
#     print(f"{domain}: {domains[domain]}")

ip_to_domains = {}
for domain, ips in domains.items():
    for ip in ips:
        ip_to_domains.setdefault(ip, []).append(domain)

for ip, domains in ip_to_domains.items():
    print(f"{ip}: {domains}")

# Created dns_search.txt
