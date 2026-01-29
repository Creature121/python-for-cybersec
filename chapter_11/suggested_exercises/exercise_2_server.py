import time
import smtpd
import asyncore


class C2_SMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        print(f"From: {mailfrom}")
        print(f"To: {rcpttos}")

        content = data.decode(errors="replace")
        print(f"Data:\n{content}")
        if "C2 data" in content:
            return "250 Received"
        return "250 Got it"


server = C2_SMTPServer(("127.0.0.1", 1025), None)  # ty:ignore[invalid-argument-type]

try:
    print("SMTP Server started. Ctrl-C to stop.")
    while True:
        asyncore.loop(timeout=1, count=1)
        time.sleep(0.01)
except KeyboardInterrupt:
    print("Server Stopped.")
