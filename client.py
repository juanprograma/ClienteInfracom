import hashlib
import socket
import time
import tqdm

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SEPARATOR = "<SEPARATOR>"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    temporalHash = hashlib.sha256()
    newHash = ""
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")
    
    start = time.time()
    received = client.recv(SIZE).decode()
    filename, filesize, clientNumber, dataHash = received.split(SEPARATOR)
    print(f"{filename}, {filesize}, {clientNumber}")
    filename = clientNumber + "-" + filename
    filesize = int(filesize)
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as file:
        while True:
            client.settimeout(0.5)
            try:
                bytes_read = client.recv(SIZE)
            except:
                break
            if not bytes_read:    
                break
            file.write(bytes_read)
            progress.update(len(bytes_read))
    file = open(filename, "rb")
    readBytes = file.read()
    newHash = hashlib.sha256(readBytes).hexdigest()
    if newHash == dataHash:
        client.send("File was received correctly".encode(FORMAT))
        print("Successful download")
    else:
        client.send("File hash doesn't match with expected hash".encode(FORMAT))
        print("File doesn't match with expected hash")
        
    end = time.time()
    recievingTime = end - start
    print(str(recievingTime))

if __name__ == "__main__":
    main()
