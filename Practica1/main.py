#Programa principal
import os
from getSNMP import consultaSNMP
from agente import *

bandera = True
agente = False

os.system('cls')
print('Sistema de Administración de Red')
while bandera:
    os.system('cls')
    print("Selecciona una opcion: ")
    print("\t 1.-Agregar dispositivo")
    print("\t 2.-Cambiar información de dispositivo")
    print("\t 3.-Eliminar dispositivo")
    print("\t 4.-Generar reporte")
    print("\t 5.-Salir")
    opc = input(': ')
    if opc == "1":
        os.system('cls')
        print('----- Agregar dispositivo -----')
        print('\n\tIndica los siguientes datos: \n')
        host = input ('Indica el nombre o host del nuevo dispositivo: ')
        host = Agente(host)
        host.setAgente()  
        agente = True
        os.system('pause')
    if opc == "2":
        os.system('cls')
        if len(host.agentes) > 0:
            host.updateAgente()
        else:
            print('AGREGA UN DISPOSITIVO')
        os.system('pause')        
    if opc == "3": 
        os.system('cls')
        if len(host.agentes) > 0:
            host.printAgentes()
            indexDel = int(input('Indica el numero del agente que deseas eliminar: '))
            host.deleteAgente(indexDel)
            print("\tEliminando reporte...")
            host.deleteReporte()
        else:
            print('NO HAY DISPOSITIVO REGISTRADO')
        os.system('pause')
    if opc == "4":
        os.system('cls')
        print('GENERAR REPORTE')
        host.generarReporte(str(host.agentes.index(host)))
        os.system('pause')
    if opc == "5":
        os.system('cls')
        print('\n\tGracias por utilizar el programa...\n')
        os.system('pause')
        bandera = False



