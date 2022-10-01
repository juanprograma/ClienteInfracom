import socket

mi_socket = socket.socket()
mi_socket.connect(('127.0.0.1',8000))

mi_socket.send("Hola desde el cliente!".encode())
respuesta = mi_socket.recv(1024)

print(respuesta)
mi_socket.close()