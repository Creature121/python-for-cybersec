import socket
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from pathlib import Path

private_key_path = Path("server_private_key.pem")
public_key_path = Path("server_public_key.pem")

if not private_key_path.exists():
    print("Didn't find server priv key file. Generating...")
    private_key = rsa.generate_private_key(65537, 2048)
    public_key = private_key.public_key()

    print("Saving keys...")
    with open(private_key_path, "wb") as f:
        f.write(
            private_key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.PKCS8,
                serialization.NoEncryption(),
            )
        )

    with open(public_key_path, "wb") as f:
        f.write(
            public_key.public_bytes(
                serialization.Encoding.PEM,
                serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )
    print("Saved.")
else:
    print("Found server priv key. Loading...")
    with open(private_key_path, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), None)
    with open(public_key_path, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    print("Loaded.")

pad_config = padding.OAEP(padding.MGF1(hashes.SHA256()), hashes.SHA256(), None)

host = "127.0.0.1"
port = 1337


def decrypt(cipher_text, private_key, padding):
    return private_key.decrypt(cipher_text, padding)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    connection, address = s.accept()
    with connection:
        data = connection.recv(256)
        plain_text = decrypt(data, private_key, pad_config)
        print(f"Received: {plain_text}")
