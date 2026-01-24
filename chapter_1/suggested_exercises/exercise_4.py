from dnslib import RR, QTYPE, time, A
from dnslib.server import DNSServer

host = "localhost"
port = 8053

subdomains = {"www.": "10.0.0.1", "smtp.": "10.0.0.2"}
domain = "example.com"
honey_subdomains = {
    "mx.": "10.0.0.3",
    "smtp.": "10.0.0.4",
    "ns.": "10.0.0.5",
    "vpn.": "10.0.0.6",
}

blocked = {}


class HoneyResolver:
    def resolve(self, request, handler):
        subdomain = str(request.q.qname.stripSuffix(f"{domain}."))
        reply = request.reply()
        if subdomain in subdomains:
            ip = subdomains[subdomain]
            reply.add_answer(
                RR(rname=request.q.qname, rtype=QTYPE.A, rclass=1, ttl=300, rdata=A(ip))
            )
        elif subdomain in honey_subdomains:
            honey_ip = honey_subdomains[subdomain]
            reply.add_answer(
                RR(
                    rname=request.q.qname,
                    rtype=QTYPE.A,
                    rclass=1,
                    ttl=300,
                    rdata=A(honey_ip),
                )
            )

        return reply


resolver = HoneyResolver()
server = DNSServer(resolver, port=port, address=host)
server.start_thread()
while True:
    time.sleep(5)
server.stop()
