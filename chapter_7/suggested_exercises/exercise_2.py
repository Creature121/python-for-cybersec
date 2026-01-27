"""
To be worked on when I actually have an FTP server running.
It is too difficult otherwise.

Q. Currently, DecoyCredentials.py sleeps between starting and terminating
a session. Add exception handling (for invalid accounts) and code to have
the code perform some actions on the target system.

"""

# import ftplib
# import telnetlib
# from time import sleep


# def FTPConnection(ip, username, password):
#     ftp = ftplib.FTP(ip, username, password)
#     sleep(5)
#     ftp.quit()


# def TelnetConnection(ip, username, password):
#     telnet = telnetlib.Telnet(ip)
#     telnet.read_until(b"login: ")
#     telnet.write(bytes(f"{username}\n", "utf-8"))
#     telnet.read_until(b"Password: ")
#     telnet.write(bytes(f"{password}\n", "utf-8"))
#     telnet.read_all()
#     sleep(1)
#     telnet.write(b"exit\n")


# ip = "3.20.135.129"
# username = "fake"
# password = "fake"
# TelnetConnection(ip, username, password)
