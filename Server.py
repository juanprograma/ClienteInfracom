import datetime
import hashlib
import socket
import threading
import time
import os

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"

def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    fileType = int(input("Ingrese 1 para enviar el archivo de 100MB o ingrese 2 para enviar el archivo de 250MB: "))
    concurrentClients = int(input("ingrese el numero de clientes que desea atender en simultaneo: "))
    barrier = threading.Barrier(concurrentClients)
    if fileType == 1:
        file = open("serverFiles/100MB.bin", "rb")
    elif fileType == 2:
        file = open("serverFiles/250MB.bin", "rb")
    fileName = os.path.basename(file.name)
    file.seek(0, os.SEEK_END)
    fileSize = file.tell()
    data = file.read()
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, barrier, data, fileName, fileSize))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

def handle_client(conn, addr, barrier, data, fileName, fileSize):
    print(f"[NEW CONNECTION] {addr} connected.")
    
    barrier.wait()
    now = datetime.datetime.now()
    print (now.strftime("%m/%d/%Y, %H:%M:%S"))
    start = time.time()
    msg = conn.send(data)
    msgHash = conn.send((hashlib.sha256(data).hexdigest()).encode(FORMAT))
    print (msgHash)
    end = time.time()
    sendingTime = end - start
    print (sendingTime)
    print(f"[{addr}] {fileName}")
    print(f"File sended: {fileName} to client {addr} with size of {fileSize} Bytes")
     
    msgFinal = conn.recv(SIZE).decode(FORMAT)
    print (f"[{addr}]: {msgFinal}")

    conn.close()

if __name__ == "__main__":
    main()
