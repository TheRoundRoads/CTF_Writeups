from find_best_move import find_best_move

'''
Main loop
'''
import socket

SERVER_IP = "54.85.45.101"
SERVER_PORT = 8006

def get_board(data):
    return list(map(int, data.split()[:16]))

def main():
    # start socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_IP, SERVER_PORT))
    
    flag_found = False
    while True:
        data = b""
        while b"): " not in data:
            data += s.recv(1024)
            if b"flag{" in data:
                flag_found = True
                break
        
        data = data.decode()
        print("Received:", data)
        
        if flag_found:
            break
        
        # extract board from data
        board = get_board(data)
        
        move = find_best_move(board)
        s.sendall(move.encode() + b"\n")
        
    
    
    
if __name__ == '__main__':
    main()
