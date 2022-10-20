from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,letter
from getSNMP import consultaSNMP
import pathlib
import os

x , y = letter

class Agente:

    agentes = []
    reportes = []
    interfaces = []

    def __init__(self,host):
        self.host = host
        self.version = ''
        self.comunidad = ''
        self.puerto = ''
        self.nombre = ''
        self.contacto = ''
        self.ubicacion = ''
        self.sistema = ''
        self.no_interfaces = 0
        self.reporte = ''
        self.archivo = ''
        self.reporte_true = False
    
    def setHost(self,host):
        self.host = host
    
    def setVersion(self,version):
        self.version = version
    
    def setComunidad(self,comunidad):
        self.comunidad = comunidad
    
    def setPuerto(self,puerto):
        self.puerto = puerto
    
    def setNombre(self,nombre):
        self.nombre = nombre
    
    def setContacto(self,contacto):
        self.contacto = contacto
    
    def setUbicacion(self,ubicacion):
        self.ubicacion = ubicacion
    
    def setSistema(self,sistema):
        self.sistema = sistema
    
    def setReporte(self,reporte):
        self.reporte = reporte

    def getHost(self):
        return self.host
    
    def getVersion(self):
        return self.version
    
    def getComunidad(self):
        return self.comunidad
    
    def getPuerto(self):
        return self.puerto

    def getNombre(self):
        return self.nombre

    def getContacto(self):
        return self.contacto    

    def getUbicacion(self):
        return self.ubicacion
    
    def getSistema(self):
        return self.sistema
    
    def getReporte(self):
        return self.reporte

    #AGREGAR DISPOSITIVO

    def setAgente(self):
        self.setVersion(input('\t\tVersión SNMP: \n'))
        self.setComunidad(input('\t\tNombre de la comunidad: \n'))
        self.setPuerto(input('\t\tPuerto: \n'))
        self.agentes.append(self)

    #EDITAR DISPOSITIVO

    def updateAgente(self):
        print('\t\t----- Editar dispositivo -----')
        print('\t\nDispositivos existentes: ')
        self.printAgentes()
        agente = int(input('\t\nIndica el numero de agente que deseas editar: '))
        if agente > len(self.agentes):
            print("\t\nOpción inválida")
        else:
            self.agentes[agente-1].setHost(input('\t\nHost: '))
            self.agentes[agente-1].setVersion(input('\t\tVersión SNMP: \n'))
            self.agentes[agente-1].setComunidad(input('\t\tNombre de la comunidad: \n'))
            self.agentes[agente-1].setPuerto(input('\t\tPuerto: \n'))
            if self.reporte_true:
                self.reportes.pop(self.reportes.index(self.getReporte()))
                self.deleteReporte()
            
    #ELIMINAR DISPOSITIVO

    def deleteAgente(self,indexDel):
        print('\t\t----- Eliminar dispositivo -----')   
        self.deleteReporte() 
        self.agentes.pop(indexDel-1)
        if self.reporte_true:
            self.reportes.pop(self.reportes.index(self.getReporte()))
            

    def deleteReporte(self):
        ruta = pathlib.Path().absolute()
        try: 
            os.remove(f'{ruta}\{self.archivo}')
        except OSError as e:
            print("*****")
                
    
    #IMPRIMIR DISPOSITIVOS

    def printAgentes(self):
        for i in range(len(self.agentes)):
            print(f'\t\nDispositivo {i+1} -->\n\t\t Host: {self.agentes[i].getHost()} \n\t\tComunidad: {self.agentes[i].getComunidad()} \n\t\tPuerto: {self.agentes[i].getPuerto()}')

    #Consultar Sistema operativo y versión

    def consultaInfo(self):
        
        info = consultaSNMP(self.getComunidad(),self.getHost(),"1.3.6.1.2.1.1.1.0")
    
        if "Windows" in info:
            self.setSistema("Windows")
            info = info[info.index('Software:')+1:]
            info = " ".join(info)
        elif "Linux" in info:
            self.setSistema("Linux")
            info = info[info.index('Linux'):info.index('Linux')+3]
            info = " ".join(info)
        else: 
            info = 'Sistema operativo no reconocido'
        
        return info
    
    #Consultar nombre de dispositivo

    def consultaNombre(self):

        self.setNombre("".join(consultaSNMP(self.getComunidad(),self.getHost(),"1.3.6.1.2.1.1.5.0")))

        return self.getNombre()

    #Consultar información de contacto

    def consultaContacto(self):

        self.setContacto("".join(consultaSNMP(self.getComunidad(),self.getHost(),"1.3.6.1.2.1.1.4.0")))

        return self.getContacto()
    
    #Consultar ubicación

    def consultaUbicacion(self):

        self.setUbicacion("".join(consultaSNMP(self.getComunidad(),self.getHost(),"1.3.6.1.2.1.1.6.0")))

        return self.getUbicacion()

    def consultaNoInterfaces(self):

        self.no_interfaces =int(("".join(consultaSNMP(self.getComunidad(),self.getHost(),"1.3.6.1.2.1.2.1.0"))))

        return self.no_interfaces    
    
    def consultaStatus(self,archivo):
        n = self.no_interfaces
        if self.no_interfaces > 5:
            n=5
        z=320
        for i in range(n):
            i+=1
            z=z+15
            x1 = f'1.3.6.1.2.1.2.2.1.7.{i}'
            y1 = int("".join(consultaSNMP(self.getComunidad(),self.getHost(),f'1.3.6.1.2.1.2.2.1.7.{i}')))
            if y1 == 1:
                archivo.drawString(100,y-z,x1)
                archivo.drawString(250,y-z,"Up")
            elif y1 == 2:
                archivo.drawString(100,y-z,x1)
                archivo.drawString(250,y-z,"Down")
            else:
                archivo.drawString(100,y-z,x1)
                archivo.drawString(250,y-z,"Testing")
        

     #Genera el reporte PDF
    
    def generarReporte(self,nombreArchivo):

        self.consultaInfo()
        self.archivo = nombreArchivo + ".pdf"
        archivo = canvas.Canvas(self.archivo, pagesize=letter)
        archivo.drawImage("IPN.jpg",50,y-100, width=75, height=75)
        archivo.drawImage("ESCOM.png",x-150,y-100, width=75, height=75)
        archivo.drawString(180,y-75,"INSTITUTO POLITÉCNICO NACIONAL")
        archivo.drawString(200,y-95,"Escuela Superior de Cómputo")
        archivo.drawString(75,y-145,"Alumno: Osvaldo Antonio Chávez Ávila")
        archivo.drawString(75,y-160,f"Sistema Operativo: {self.consultaInfo()}")
        archivo.drawImage(f"{self.getSistema()}.jpg",x-350,y-230, width=65, height=65)
        archivo.drawString(75,y-260,f"Nombre de dispositivo: {self.consultaNombre()}")
        archivo.drawString(75,y-275,f"Contacto: {self.consultaContacto()}")
        archivo.drawString(75,y-290,f"Ubicación: {self.consultaUbicacion()}")
        archivo.drawString(75,y-305,f"Numero de interfaces: {self.consultaNoInterfaces()}")
        archivo.drawString(100,y-320,"Interfaz")
        archivo.drawString(250,y-320,"Estatus")
        self.consultaStatus(archivo)
        archivo.showPage()
        archivo.save()
        self.reportes.append(archivo)
        self.setReporte(archivo)
        self.reporte_true = True
        print(self.reportes)
        
    
        
        
