#!/usr/bin/env python3

import socket
import os # Para "toque una tecla para continuar"
import sys #Para salir del programa

HOST = print("\nIngrese la dirección IP del servidor:\t")   # The server's hostname or IP address
PORT = 65432  # The port used by the server
buffer_size = 1024


#Funciones para el juego del buscaminas
def imprimirTablero(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            print(matriz[i][j], end=" ")
        print()
    print()

def generarTableroCliente(n, dificultad):
    if dificultad == 'f':
        tableroCabecera = [" ","A","B","C","D","E","F","G","H","I"]
        tableroColumna = [" ", 0,1,2,3,4,5,6,7,8]
    else:
        tableroCabecera = [" "," A","B","C","D","E","F","G","H","I", "J", "K", "L", "M","N", "O", "P"]
        tableroColumna = [" ", " 0"," 1"," 2"," 3"," 4"," 5"," 6"," 7"," 8"," 9",10,11,12,13,14,15]
    tableroCliente = [[ "*" for x in range(n+1)] for x in range(n+1)]
    for i in range(1):
        for j in range(len(tableroCliente[i])):
            if tableroCliente[i][j] == "*":
                tableroCliente[i][j] = tableroCabecera[j]
                tableroCliente[j][i] = tableroColumna[j]
    return tableroCliente

def actualizarTableroCliente(tableroCliente, CooX, CooY, toque):
    print("Actualizo tablero del cliente")
    if toque == 0:
        for i in range(len(tableroCliente)):
            tableroCliente[CooX+1][CooY] = "-"
    else:
        tableroCliente[CooX+1][CooY] = "X"
    imprimirTablero(tableroCliente)

def verificarToqueMina(tableroCliente, CooX, CooY):
    CooYj=0;
    #Buscamos el numero de la letra para obtener la coordenada de la mina
    for i in range(1):
        for j in range (len(tableroCliente[i])):
            if tableroCliente[i][j].strip() == CooY:
                CooYj = j
                actualizarTableroCliente(tableroCliente, CooX, CooYj, 1)
                break


#Aqui empieza la comunicacion entre el cliente y el servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    mensajeInicial = """
    =======================================================
    ***************** Aplicación Cliente *****************
    =======================================================
    """
    print(mensajeInicial)
    #Solicto la partida
    mensajeEnviar = "Deseo jugar una partida de buscaminas"
    TCPClientSocket.send(mensajeEnviar.encode(encoding="ascii", errors="ignore"))
    mensajeRecibido = TCPClientSocket.recv(buffer_size)
    print("Servidor: ", mensajeRecibido.decode(encoding="ascii", errors="ignore"))
    #Respondo a la dificultad
    mensajeEnviar = input("Cliente: ")
    TCPClientSocket.send(mensajeEnviar.encode(encoding="ascii", errors="ignore"))
    mensajeRecibido = TCPClientSocket.recv(buffer_size)
    #Generamos el tablero del cliente
    if mensajeEnviar == 'f':
        print("Escogio fácil")
        tableroCliente = generarTableroCliente(9, mensajeEnviar)
        imprimirTablero(tableroCliente)
    else:
        print("Escogió dificil")
        tableroCliente = generarTableroCliente(16, mensajeEnviar)
        imprimirTablero(tableroCliente)
    print("Servidor: ", mensajeRecibido.decode(encoding="ascii", errors="ignore"))
    mensajeEnviar = "Estoy listo..."
    TCPClientSocket.send(mensajeEnviar.encode(encoding="ascii", errors="ignore"))
    mensajeEnviar = input("Cliente: ")
    TCPClientSocket.send(mensajeEnviar.encode(encoding="ascii", errors="ignore"))
    mensajeRecibido = TCPClientSocket.recv(buffer_size)
    print("Servidor: ", mensajeRecibido.decode(encoding="ascii", errors="ignore"))
    while True:
        #Vamos a solicitar una partida
        mensajeEnviar = input("Cliente: ")
        # print(f"{mensajeEnviar[0]} {mensajeEnviar[1]} {mensajeEnviar[2]}")
        verificarToqueMina(tableroCliente,int(mensajeEnviar[0]), mensajeEnviar[2].upper())
        TCPClientSocket.send(mensajeEnviar.encode(encoding="ascii", errors="ignore"))
        mensajeRecibido = TCPClientSocket.recv(buffer_size)
        if mensajeRecibido.decode(encoding="ascii", errors="ignore") == "True":
            tuplaMinas = TCPClientSocket.recv(buffer_size)
            #tupla minas
            print("Tocó una mina, ¡Fin del juego!")
            print("Al continuar se saldrá del programa")
            os.system("Pause")
            sys.exit()
        else:
            #actualizo tablero
            print("Servidor: ", mensajeRecibido.decode(encoding="ascii", errors="ignore"))
            imprimirTablero(tableroCliente)
    # TCPClientSocket.close()
