import socket

mi_socket = socket.socket()
mi_socket.bind(('127.0.0.1',8000))
mi_socket.listen(5)

while True:
        conexion, addr = mi_socket.accept()
        print("Nueva conexion establecida!")
        print(addr)

        peticion = conexion.recv(1024)
        print(peticion)

        conexion.send("Hola, te saludo desde el servidor".encode())
        conexion.close()

mi_socket.close()
