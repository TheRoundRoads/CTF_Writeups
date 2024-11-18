import socket
import json
import math
from Crypto.Util.number import inverse
import time

# RSA public parameters
# Corrected modulus n = p * q
p = 9727707634026882185733922354917544266339734201376617114850662457253634956271004197770350810145775489 # Hidden
q = 3124318476101471610798641177344759107063873312304118809566534382213883689581536970918237820746041309 # Hidden
n = 30392456691103520456566703629789883376981975074658985351907533566054217142999128759248328829870869523368987496991637114688552687369186479700671810414151842146871044878391976165906497019158806633675101
e = 65537

SERVER_IP = "54.85.45.101"  # Replace with actual server IP
SERVER_PORT = 8010      # Replace with actual server port

def get_hex(data):
    # extract hex from received bytes
    start = data.index("0x")
    end = data.index("\n")
    
    return int(data[start:end], 16)

def get_decryption(ciphertext_hex):
    # start socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, SERVER_PORT))
    
    # receive first part
    data = b''
    while b'in hex format:' not in data:
        data = s.recv(1024)  # first recv
        
    # set flags to stop while loop
    correct, faulty = False, False
    correct_decryption, faulty_decryption = None, None
    while not (correct and faulty):
        s.sendall(ciphertext_hex.encode() + "\n".encode())
        data = ""
        while "in hex format:\n" not in data:
            data += s.recv(1024).decode()
        # print("Received:", data)
        
        # update flags
        if "Fault" in data:
            faulty = True
            faulty_decryption = get_hex(data)
        else:
            correct = True
            correct_decryption = get_hex(data)
            
        time.sleep(0.1)
            
        
    s.shutdown(socket.SHUT_WR)
    print("Connection closed.")
    s.close()
    print("Correct:", correct_decryption)
    print("Faulty:", faulty_decryption)
    return correct_decryption, faulty_decryption

def attack():
    # multiple random hex strings to attack with
    ciphertext_hex = ["0xdeadbeef", "0x1234567", "0xabc67318", "0x36caef", "0x88172ff"]
    
    # approach is to find difference between correct and faulty, it is divisible by p.
    # so we find multiple differences, then find the gcd. The gcd is either p, or has p as divisor
    gcd = float('inf')
    for ct in ciphertext_hex:
        print("Trying for ct:", ct)
        correct_decryption, faulty_decryption = get_decryption(ct)
        # Calculate the difference
        delta = abs(correct_decryption - faulty_decryption)
        if gcd == float('inf'):
            gcd = delta
        else:
            gcd = math.gcd(gcd, delta)
    
    # best case: gcd is p
    if n % gcd == 0:
        return gcd, n // gcd
    
    print("probably won't reach here")
    # find p from gcd
    for i in reversed(range(2, int(gcd**0.5)+1)):
        if gcd % i == 0:
            p = i
            if n % p == 0:
                return p, n//p
    
    return None, None

def decrypt(c_hex, p, q):
    c = int(c_hex, 16)
    # Ensure n is correct
    assert p * q == n

    phi = (p - 1) * (q - 1)
    d = inverse(e, phi)

    dP = d % (p - 1)
    dQ = d % (q - 1)
    qInv = inverse(q, p)

    # Decrypt using CRT
    m1 = pow(c, dP, p)
    m2 = pow(c, dQ, q)
    # Combine using CRT
    h = (qInv * (m1 - m2)) % p
    m = (m2 + h * q) % n
    return m

# Run the attack
p, q = attack()
print(f"p={p}, q={q}")

flag = "0x3939dad4ba6dfe1d4c203e9c2acfde66493cac762d80114c7f740af92268725b7b16afd060594dd0153b26d7651be7e50061a4149d718e5b51305925dfb237844ee231d418e005aaa0701297c79e9a5e144ab0"
m = decrypt(flag, p, q)
print(m.to_bytes(length=30).decode())