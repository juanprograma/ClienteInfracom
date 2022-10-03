import hashlib
import socket
import time

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")
    
    start = time.time()
    msg = client.recv(SIZE).decode(FORMAT)
    newHash = hashlib.sha256(msg.encode(FORMAT)).hexdigest()
    print(msg)
    print(newHash)
    msgHash = client.recv(SIZE).decode(FORMAT)
    print (msgHash)
    end = time.time()
    recievingTime = start - end
    print(recievingTime)
    if newHash == msgHash:
        client.send("File was recieved correctly".encode(FORMAT))
        print("Successful download")
    else:
        client.send("File hash doesn't match with expected hash".encode(FORMAT))
        print("File doesn't match with expected hash")

if __name__ == "__main__":
    main()
