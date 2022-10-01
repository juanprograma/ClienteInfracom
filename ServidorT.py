import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 8000
ADDR = (IP, PORT)
TAMANO = 1024
FORMATO = "utf-8"
MSG_DESCONEXION = "!DESCONECTAR"

def handle_client(conn, addr):
    print(f"[NUEVA CONEXION] {addr} conectada")
    conectada = True
    
    while conectada:
        msg = conn.recv(TAMANO).decode(FORMATO)
        if msg == MSG_DESCONEXION:
            conectada = False
            
        print (f"[{addr}] {msg}")
        msg = f"Mensaje recibido: {msg}"
        conn.send(msg.encode(FORMATO))
        
    conn.close()

def main():
    print("[INICIALIZANDO] El servidor se esta inicializando...")
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(ADDR)
    servidor.listen()
    print(f"[ESCUCHANDO] El servidor esta escuchando en {IP}:{PORT}")
    
    while True:
        conn, addr = servidor.accept()
        hilo = threading.Thread(target=handle_client, args=(conn, addr))
        hilo.start()
        print(f"[CONEXIONES ACTIVAS] {threading.activeCount() - 1}")