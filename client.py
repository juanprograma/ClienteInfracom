import socket
import time

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")
    
    start = time.time()
    msg = client.recv(SIZE).decode(FORMAT)
    msgHash = client.recv(SIZE).decode(FORMAT)
    end = time.time()
    recievingTime = start - end
    newHash = hash(msg)
    if newHash == msgHash:
        client.send("File was recieved correctly".encode(FORMAT))
        print("Successful download")
    else:
        client.send("File hash doesn't match with expected hash".encode(FORMAT))
        print("File doesn't match with expected hash")

if __name__ == "__main__":
    main()
