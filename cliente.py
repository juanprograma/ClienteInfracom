import socket

mi_socket = socket.socket()
mi_socket.bind(('localhost',81))

mi_socket.send("Hola desde el cliente!".encode())
respuesta = mi_socket.recv(1024)

print(respuesta)
mi_socket.close()