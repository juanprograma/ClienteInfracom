import datetime
import hashlib
import socket
import threading
import time
import os

import tqdm

IP = socket.gethostbyname(socket.gethostname())
PORT = 5566
ADDR = (IP, PORT)
SIZE = 2048
FORMAT = "utf-8"
SEPARATOR = "<SEPARATOR>"

def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    fileType = int(input("Ingrese 1 para enviar el archivo de 100MB o ingrese 2 para enviar el archivo de 250MB: "))
    concurrentClients = int(input("Ingrese el numero de clientes que desea atender en simultaneo: "))
    barrier = threading.Barrier(concurrentClients)
    temporalHash = hashlib.sha256()
    dataHash = ""
    if fileType == 1:
        file = open("serverFiles/100MB.bin", "rb")
    elif fileType == 2:
        file = open("serverFiles/250MB.bin", "rb")
    for chunk in iter(lambda: file.read(SIZE), b''):
        temporalHash.update(chunk)
        dataHash += temporalHash.hexdigest()
    fileName = os.path.basename(file.name)
    file.seek(0, os.SEEK_END)
    fileSize = file.tell()
    file.close()
    print(f"The file {fileName} with {fileSize} Bytes was loaded and its hash was calculated")
    clientCount = 1
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, barrier, dataHash, fileName, fileSize, clientCount))
        clientCount+= 1
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

def handle_client(conn, addr, barrier, dataHash, fileName, fileSize, clientNumber):
    print(f"[NEW CONNECTION] {addr} connected.")
    barrier.wait()
    now = datetime.datetime.now()
    print (now.strftime("%m/%d/%Y, %H:%M:%S"))
    start = time.time()
    conn.send(f"{fileName}{SEPARATOR}{fileSize}{SEPARATOR}{clientNumber}{SEPARATOR}{dataHash}".encode())
    progress = tqdm.tqdm(range(fileSize), f"Sending {fileName}", unit="B", unit_scale=True, unit_divisor=1024)
    with open("serverFiles/" + fileName, "rb") as file:
        while True:
            bytes_read = file.read(SIZE)
            if not bytes_read:
                break
            conn.sendall(bytes_read)
            progress.update(len(bytes_read))
    print(f"[{addr}] {fileName}")
    print(f"File sended: {fileName} to client {addr} with size of {fileSize} Bytes")
    msgFinal = conn.recv(SIZE).decode(FORMAT)
    print (f"[{addr}]: {msgFinal}")
    end = time.time()
    sendingTime = end - start
    print(str(sendingTime))

    conn.close()

if __name__ == "__main__":
    main()
