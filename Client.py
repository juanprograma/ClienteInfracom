import socket
#Donde queremos conectarnos
#Mismos valores del servidor
host = '127.0.0.1'
port = 1234

#Conexión con el socket del servidor
ClientSocket = socket.socket()
print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

#Comunicación con el servidor
Response = ClientSocket.recv(2048)
while True:
    Input = input('Your message: ')
    ClientSocket.send(str.encode(Input))
    Response = ClientSocket.recv(2048)
    print(Response.decode('utf-8'))

ClientSocket.close()