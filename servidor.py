import socket

mi_socket = socket.socket()
mi_socket.bind(('localhost',81))
mi_socket.listen(25)

while True:
        conexion, addr = mi_socket.accept()
        print("Nueva conexion establecida!")
        print(addr)

        peticion = conexion.recv(1024)
        print(peticion)

        conexion.send("Hola, te saludo desde el servidor")
        conexion.close()

mi_socket.close()
