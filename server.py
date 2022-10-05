from calendar import month
import datetime
from fileinput import filename
import hashlib
import socket
import threading
import time
import os
import tqdm

IP = '192.168.137.130'
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
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
    readBytes = file.read()
    dataHash = hashlib.sha256(readBytes).hexdigest()
    fileName = os.path.basename(file.name)
    fileSize = os.path.getsize("serverFiles/" + fileName)
    file.close()
    print(f"The file {fileName} with {fileSize} Bytes was loaded and its hash was calculated")
    clientCount = 1
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, barrier, dataHash, fileName, fileSize, clientCount,concurrentClients))
        clientCount+= 1
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

def handle_client(conn, addr, barrier, dataHash, fileName, fileSize, clientNumber,concurrentClients):
    print(f"[NEW CONNECTION] {addr} connected.")
    barrier.wait()
    now = datetime.datetime.now()
    successful = False
    print (now.strftime("%m/%d/%Y, %H:%M:%S"))
    start = time.time()
    conn.send(f"{fileName}{SEPARATOR}{fileSize}{SEPARATOR}{clientNumber}{SEPARATOR}{concurrentClients}{SEPARATOR}{dataHash}".encode())
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
    if msgFinal == 'File was received correctly':
        successful = True
    end = time.time()
    sendingTime = end - start
    print(str(sendingTime))
    
    year = str(now)[:4]
    month = str(now)[5:7]
    day = str(now)[8:10]
    hour = str(now)[11:13]
    minute = str(now)[14:16]
    second = str(now)[17:19]
    concurrentClients = str(concurrentClients)
    
    numPrueba = 0
    if concurrentClients == str(1):
        if str(fileSize) == str(104857600):
            numPrueba = 1
        elif str(fileSize) ==str(250000000):
            numPrueba = 2
    elif concurrentClients == str(5):
        if str(fileSize) == str(104857600):
            numPrueba = 3
        elif str(fileSize) == str(250000000):
            numPrueba = 4
    elif concurrentClients == str(10):
        if str(fileSize) == str(104857600):
            numPrueba = 5
        elif str(fileSize) == str(250000000):
            numPrueba = 6

    filename = 'Cliente'+ str(clientNumber) + "-Prueba" + str(numPrueba) + '-' + str(concurrentClients)
    save_path = 'Logs/'
    file_name = 'S'+ str(clientNumber)+ year + '-' + month + '-' + day + '-' + hour + '-' + minute + '-' + second + '-log.txt' 
    completeName = os.path.join(save_path,file_name)
    newFile = open(completeName, 'w')
    newFile.write('El archivo enviado fue: ' + filename +'\n')
    newFile.write('El archivo tiene un tamaño de: ' + str(fileSize) + ' bytes\n')
    newFile.write('El cliente al que le fue enviado es: ' + str(clientNumber) +'\n')
    newFile.write('El tiempo de transferencia para este cliente fue: ' + str(sendingTime)+' segundos\n')
    if successful == True:
        newFile.write('La entrega fue exitosa\n')
    elif successful == False:
        newFile.write('La entrega no fue exitosa\n')
    

    conn.close()

if __name__ == "__main__":
    main()
