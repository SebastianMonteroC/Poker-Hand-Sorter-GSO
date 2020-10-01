"""
Escuela de Ciencias de la Computación e infomática | Universidad de Costa Rica
Proyecto I Programación Paralela y Concurrente | CI-0117 | II-Semestre 2020
Profesor: Alan Calderón Castro
Estudiantes: Carlos Espinoza Peraza B92786 y Sebastián Montero Castro B95016

Descripción del proyecto:
    
"""

from mpi4py import MPI
import sys, getopt
import numpy as np

#Atributos globales
DIMENSION = 10

#Clase Gusano con X atributos
class Gusano:
    def __init__(self,L):
        self.nLuciferina = L
        self.pos = np.random.randint(1,13,(DIMENSION))
        self.vAdaptacion = 0.0
        self.cCubierto = [] #Modificar por un numpy array
        self.intraD = 0.0

    def getNLuciferina(self):
        return self.nLuciferina

    def getPos(self):
        return self.pos

    def getVAdaptacion(self):
        return self.vAdaptacion
    
    def getCCubierto(self):
        return self.cCubierto
    
    def getIntraD(self):
        return self.intraD
    
    def setNLuciferina(self,L):
        self.nLuciferina = L
    
    def setPos(self, pos):
        self.pos = pos
    
    def setVAdaptacion(self, vAdaptacion):
        self.vAdaptacion = vAdaptacion
    
    def setCCubierto(self, cCubierto):
        self.cCubierto = cCubierto
    
    def setIntraD(self, intraD):
        self.intraD = intraD
    

    
#Carga los datos de un archivo de texto y los parsea para crear un arreglo numpy
def cargarDatos():
    data = []
    file = open("poker-hand-training-true.data", "r")
    lineas = 0
    for line in file:
        lineas += 1
        cLine = line.split(",")
        fila = []
        for i in range(0,10):
            fila.append(int(cLine[i]))
        data.append(fila)
    file.close()
    data = np.array(data)
    #print(self.data[1])
    return data, lineas

#Genera las listas invertidas
def generarListaInvertida(data):
    for i in range(len(data)):
        for j in range(len(data[0])):
            pass

def fitness(gusanos):  
    pass


#Se encarga de recibir el valor de los parámetros por consola
def getValores(argv):

    #Atributos que se desean pasar por consola
    r = ""
    g = ""
    s = ""
    i = ""
    l = ""
    k = ""
    m = ""
    
    try:
        #Se guardan en un tupla la etiqueta(opt) y el valor (arg)
        opts, args = getopt.getopt(argv, "h:r:g:s:i:l:k:m:", ["H=","R=","G=","S=","I=","L=","K=","M="]) #Para agragar parámetros se debe modificar el parámetro "h:r:" -> "h:r:a:b:c:"... y la lista ["H=","R="] -> ["H=","R=","A=","B=","C="]
    except getopt.GetoptError:
        print("-r <tasa constante de decremento de luciferina\n-g <fracción constante de incremento de lciferina>\n-s <distancia constante en que se mueven los gusanos>\n-i <rango de cobertura>\n-l <valor inicial de luciferina>\n-k <cantidad de clases que debe encontrar>\n-m <tasa de gusanos por dato>")
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == "-h":            #Revisa si le pasaron un -h el cual despliega el mensaje de ayuda
            print("Imprimir el -h despliega la ayuda para ver que parámetros recibe por consola")
            sys.exit()
        elif opt in ("-r", "--R"): #Revisa si la etiqueta coincide y guarda el valor en el atributp correspondiente
            r = arg
        elif opt in ("-g", "--G"): #Revisa si la etiqueta coincide y guarda el valor en el atributp correspondiente
            g = arg
        elif opt in ("-s", "--S"): #Revisa si la etiqueta coincide y guarda el valor en el atributp correspondiente
            s = arg
        elif opt in ("-i", "--I"): #Revisa si la etiqueta coincide y guarda el valor en el atributp correspondiente
            i = arg
        elif opt in ("-l", "--L"): #Revisa si la etiqueta coincide y guarda el valor en el atributp correspondiente
            l = arg
        elif opt in ("-k", "--K"): #Revisa si la etiqueta coincide y guarda el valor en el atributp correspondiente
            k = arg
        elif opt in ("-m", "--M"): #Revisa si la etiqueta coincide y guarda el valor en el atributp correspondiente
            m = arg
    
    return float(r), float(g), float(s), float(i), float(l), float(k), float(m) #Retorna el valor para ser usado

#Función principal para mis panas
def main(argv):
    comm = MPI.COMM_WORLD #Comunicador
    pid = comm.rank       #Proceso
    size = comm.size      #Cantidad de procesos
    R = 0                 #Tasa constante de decremento de luciferina
    G = 0                 #Fracción constante de incremento de luciferina
    S = 0                 #Distancia constante en la que se mueven los gusanos
    I = 0                 #Rango de cobertura de un gusano para incluir datos asociados
    L = 0                 #Valor inicial de luciferina en los gusanos
    K = 0                 #Cantidad de clases a encontrar
    M = 0                 #Tasa de gusanos por dato
    data = []             #Conjunto de manos
    cant_gusanos = 0
    gusanos = []

    if pid == 0:
        #R, G, S, I, L, K, M = getValores(argv) #Guardar un valor dado por consola
        data, cant_datos = cargarDatos()
        cant_gusanos = int(cant_datos * 0.9)
    
    data, cant_gusanos = comm.bcast(data,cant_gusanos)

    inicio = pid * cant_gusanos / size
    final = cant_gusanos / size + inicio

    for i in range(inicio, final):
        g = Gusano(5.0)
        gusanos.append(g)

    gusanos = comm.reduce(gusanos,op = MPI.SUM)

    if pid == 0:
        print(len(gusanos))

    




    
    if pid == 0:
        #print(R, " ", G, " ", S, " ", I, " ", L, " ", K, " ",M)
        #g.printA()
        pass
    
if __name__ == "__main__":
    main(sys.argv[1:])