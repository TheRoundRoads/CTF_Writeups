import socket
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Server connection details
SERVER_IP = "54.85.45.101"  # Replace with actual server IP
SERVER_PORT = 8001       # Replace with actual server port

# X25519 key size
X25519_KEY_SIZE = 32

# Create the client public key as all zeros
client_pub = bytes([0] * X25519_KEY_SIZE)

# Prepare the payload to send to the server
payload = json.dumps({"client_pub": client_pub.hex()}).encode()

# Send the payload to the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((SERVER_IP, SERVER_PORT))
    sock.sendall(payload)
    
    # Receive the server's response
    response = sock.recv(4096)
    
    # Print the server's response
    iv_ct = json.loads(response.decode())
    print("Server Response:", response.decode())

iv = bytes.fromhex(iv_ct["iv"])
ct = bytes.fromhex(iv_ct["ct"])
cipher = Cipher(algorithms.AES(client_pub), modes.CTR(iv))
decryptor = cipher.decryptor()
original = decryptor.update(ct)
print(original.decode())