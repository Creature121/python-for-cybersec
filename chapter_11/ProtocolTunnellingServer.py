from http.server import BaseHTTPRequestHandler, HTTPServer
from base64 import b64decode, b64encode


class C2Server(BaseHTTPRequestHandler):
    def do_GET(self):
        data = b64decode(self.headers["Cookie"]).decode("utf-8").rstrip()
        print(f"Received: {data}")

        if data == "C2 data":
            response = b64encode(bytes("Received", "utf-8"))
            self.send_response(200)
            self.end_headers()
            self.wfile.write(response)
        else:
            self.send_error(404)


if __name__ == "__main__":
    hostname = ""
    port = 8443
    web_server = HTTPServer((hostname, port), C2Server)
    try:
        web_server.serve_forever()
    except KeyboardInterrupt:
        pass

    web_server.server_close()
