import socket
from Crypto.Cipher import AES

host = "127.0.0.1"
port = 1337

key = b"Sixteen byte key"


def decrypt(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(data)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    connection, address = s.accept()
    with connection:
        iv = connection.recv(16)
        length = connection.recv(1)
        data = connection.recv(1024)
        while d := connection.recv(1024):
            data += d
        plain_text = decrypt(data, key, iv).decode("utf-8")[: ord(length)]
        print(f"Received: {plain_text}")
