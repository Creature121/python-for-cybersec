import smtplib

smtp_host = "127.0.0.1"
smtp_port = 1025

from_address = "milan@email.com"
to_address = "alan@mine.com"


message = """\
From: milan@email.com
To: alan@mine.com

Hi from Milan to Alan.


"""

data = "C2 data"
message += data

with smtplib.SMTP(smtp_host, smtp_port) as server:
    server.set_debuglevel(1)
    server.sendmail(from_address, to_address, message)
