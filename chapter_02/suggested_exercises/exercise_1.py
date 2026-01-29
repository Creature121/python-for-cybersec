import paramiko
import telnetlib
import socket

# Packages for exercise 1
from ftplib import FTP
from smtplib import SMTP, SMTPAuthenticationError


def SSHLogin(host, port, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=username, password=password)
        ssh_session = ssh.get_transport().open_session()

        if ssh_session.active:
            print(
                f"SSH login successful on {host}:{port} with username {username} and password {password}"
            )

        ssh.close()
    except:  # noqa: E722
        print(f"SSH login failed {username} {password}")


def TelnetLogin(host, port, username, password):
    telnet = telnetlib.Telnet(host, port, timeout=1)
    telnet.read_until(b"login: ")
    telnet.write((f"{username}\n").encode("utf-8"))
    telnet.read_until(b"Password: ")
    telnet.write((f"{password}\n").encode("utf-8"))

    try:
        result = telnet.expect([b"Last Login"])
        if result[0] > 0:
            print(
                f"Telnet login successful on {host}:{port} with username {username} and password {password}"
            )
        telnet.close()
    except (EOFError, socket.timeout):
        print(f"Telent login failed {username} {password}")


def FTPLogin(host, port=21, username="anonymous", password=""):
    ftp = FTP()
    ftp.connect(host, port)
    result = ftp.login(user=username, passwd=password)
    try:
        if result.startswith("230"):
            print(
                f"FTP login successful on {host}:{port} with username {username} and password {password}"
            )
            ftp.close()
    except:  # noqa: E722
        print(f"FTP login failed {username} {password}")


def SMTPLogin(host, port, username, password):
    smtp = SMTP()
    smtp.connect(host, port)
    try:
        smtp.login(username, password)
        print(
            f"SMTP login successful on {host}:{port} with username {username} and password {password}"
        )
        smtp.close()
    except SMTPAuthenticationError:
        pass
    except:  # noqa: E722
        print(f"SMTP login failed {username} {password}")


host = "127.0.0.1"
ssh_port = 2200
telnet_port = 23
ftp_port = 21
smtp_port = 25

with open("defaults.txt", "r") as f:
    for line in f:
        vals = line.split()
        username = vals[0].strip()
        password = vals[1].strip()
        SSHLogin(host, ssh_port, username, password)
        TelnetLogin(host, telnet_port, username, password)
        FTPLogin(host, ftp_port, username, password)
        SMTPLogin(host, smtp_port, username, password)
