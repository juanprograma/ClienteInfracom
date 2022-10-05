import hashlib
import socket
import time
import tqdm
import datetime
import os

#IP = '192.168.137.130'
IP = '192.168.1.117'
PORT = 5566
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SEPARATOR = "<SEPARATOR>"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    temporalHash = hashlib.sha256()
    newHash = ""
    #print(ADDR)
    client.connect(ADDR)
    print(f"[CONNECTED] Client connected to server at {IP}:{PORT}")
    
    now = datetime.datetime.now()
    successful = False
    start = time.time()
    received = client.recv(SIZE).decode()
    filename, filesize, clientNumber, concurrentClients, dataHash = received.split(SEPARATOR)
    print(f"{filename}, {filesize}, {clientNumber}")
    concurrentClients = concurrentClients
    #print('tamaño' + filesize,concurrentClients)
    #print(concurrentClients)
    numPrueba = 0
    if concurrentClients == str(1):
        if filesize == str(104857600):
            numPrueba = 1
        elif filesize ==str(250000000):
            numPrueba = 2
    elif concurrentClients == str(5):
        if filesize == str(104857600):
            numPrueba = 3
        elif filesize == str(250000000):
            numPrueba = 4
    elif concurrentClients == str(10):
        if filesize == str(104857600):
            numPrueba = 5
        elif filesize == str(250000000):
            numPrueba = 6
    filename = 'Cliente'+ clientNumber + "-Prueba" + str(numPrueba) + '-' + concurrentClients
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
        successful = True
    else:
        client.send("File hash doesn't match with expected hash".encode(FORMAT))
        print("File doesn't match with expected hash")
        
    end = time.time()
    recievingTime = end - start
    print(str(recievingTime))

    year = str(now)[:4]
    month = str(now)[5:7]
    day = str(now)[8:10]
    hour = str(now)[11:13]
    minute = str(now)[14:16]
    second = str(now)[17:19]
    
    save_path = 'Logs/'
    file_name = 'C'+year + '-' + month + '-' + day + '-' + hour + '-' + minute + '-' + second + '-log.txt' 
    completeName = os.path.join(save_path,file_name)
    newFile = open(completeName, 'w')
    newFile.write('El archivo enviado fue: ' + filename +'\n')
    newFile.write('El archivo tiene un tamaño de: ' + str(filesize) + ' bytes\n')
    newFile.write('El cliente al que le fue enviado es: ' + clientNumber +'\n')
    newFile.write('El tiempo de transferencia para este cliente fue: ' + str(recievingTime)+' segundos\n')
    if successful == True:
        newFile.write('La entrega fue exitosa\n')
    elif successful == False:
        newFile.write('La entrega no fue exitosa\n')

if __name__ == "__main__":
    main()
