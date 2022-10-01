import socket
from _thread import *

#En los que nos queremos comunicar
host = '127.0.0.1' 
port = 1234
ThreadCount = 0

#Manejador de Cliente
#Devuelve el mismo mensaje al cliente
def client_handler(connection):
    connection.send(str.encode('You are now connected to the replay server...'))
    while True:
        data = connection.recv(2048) #Para recibir mensajes del cliente
        message = data.decode('utf-8')
        if message == 'BYE': #El cliente corta la comunicación
            break
        reply = f'Server: {message}'
        connection.sendall(str.encode(reply))
    connection.close()

#El servidor acepta conexiones del cliente
#Abre un nuevo thread para cada cliente
def accept_connections(ServerSocket):
    Client, address = ServerSocket.accept()
    print(f'Connected to: {address[0]}:{str(address[1])}')
    start_new_thread(client_handler, (Client, )) 

#Inicializar
def start_server(host, port):
    #Creación del socket
    ServerSocket = socket.socket()
    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))
    print(f'Server is listing on the port {port}...')
    ServerSocket.listen()

    while True:
        accept_connections(ServerSocket)
start_server(host, port)