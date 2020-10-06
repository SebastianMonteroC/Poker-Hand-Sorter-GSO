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
import random
import math

#Atributos globales
DIMENSION = 10

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

#Clase Gusano con X atributos
class Gusano:
    def __init__(self,L,pos):
        self.nLuciferina = L
        self.pos = pos
        self.vAdaptacion = 0.0
        self.cCubierto = [] #Modificar por un numpy array
        self.intraD = 0.0

    def sacarConjuntoCubierto(self,r,listaInv,datos):
        conjuntoFinal = []
        conjuntoFinal = np.array(conjuntoFinal, dtype = int)
        for i in range(0,10,2):
            conjuntoAux = []
            conjuntoAux = np.array(conjuntoAux, dtype = int)

            minX = math.ceil(self.pos[i]) - r
            maxX = int(self.pos[i]) + r
            minY = math.ceil(self.pos[i+1]) - r
            maxY = int(self.pos[i+1]) + r

            if(minX < 1):
                minX = 1
            if(maxX > 4):
                maxX = 4
            if(minY < 1):
                minY = 1
            if(maxY > 13):
                maxY = 13
            
            conjuntoAux = []
            conjuntoAux = np.array(conjuntoAux, dtype = int)

            for j in range(minX,maxX + 1):
                for k in range(minY,maxY + 1):
                    conjuntoAux = np.concatenate([conjuntoAux,listaInv[j-1][k-1][int((i+1)/2)]])
            if(len(conjuntoFinal) == 0):
                conjuntoFinal = conjuntoAux
            else:
                conjuntoFinal = np.intersect1d(conjuntoFinal,conjuntoAux)


            if len(conjuntoFinal) == 0:
                break
        
        for i in range(len(conjuntoFinal)):
            dato = conjuntoFinal[i]
            dist = distanciaEuc(self.pos,datos[conjuntoFinal[i]])
            if dist > r :
                np.delete(conjuntoFinal,i) 

        self.cCubierto = conjuntoFinal

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
    
    def setIntraD(self,data):
        intraD = 0
        for i in range(len(self.cCubierto)):
            intraD += distanciaEuc(self.pos,data[self.cCubierto[i]])
        self.intraD = intraD
    
def distanciaEuc(pos1,pos2):
    distancia = 0.0
    for i in range(DIMENSION):
        distancia += math.sqrt(pow((pos1[i] - pos2[i]),2))
    return distancia

def randomPos(proc,size):
        rPos = []
        for i in range (1,11):
            if i % 2 != 0:
                rPos.append(random.uniform(1,4))
            else:
                rPos.append(random.uniform(1,13))
        rPos = np.array(rPos)

        return rPos
    
#Carga los datos de un archivo de texto y los parsea para crear un arreglo numpy
def cargarDatos():
    data = []
    file = open("poker-hand-training-true.data", "r") #poker-hand-training-true.data
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
    return data, lineas

#Genera las listas invertidas
def generarListaInvertida(data): #[4][13][5]
    listaInvertida = []
    for i in range(4):
        d1 = []
        for j in range(13):
            d2 = []
            for k in range(5):
                d2.append(0)
            d1.append(d2)
        listaInvertida.append(d1)
    
    for i in range(4):
        for j in range(13):
            for k in range(0,10,2):
                listaIndices = []
                for l in range(len(data)):
                    if data[l][k] == i+1 and data[l][k+1] == j+1 :
                        listaIndices.append(l)
                listaInvertida[i][j][int((k + 1) / 2)] = listaIndices
    verListaInvertida(listaInvertida)
    
    return listaInvertida

def verListaInvertida(lInv):
    contador = 0
    for i in range(len(lInv)):
        for j in range(len(lInv[i])):
            for k in range(len(lInv[i][j])):
                contador = contador + len(lInv[i][j][k])
                #print("[",i+1,"]","[",j+1,"]","[",k+1,"] = ", str(lInv[i][j][k]))
    print(contador)
    
def fitness(gusanos):  
    pass

def distIntra(gus):
    m_dist = []
    for i in range(len(gus)):
        d1 = []
        for j in range(len(gus)):
            d1.append(distanciaEuc(gus[i].getPos(),gus[j].getPos()))
        m_dist.append(d1)
    
    print(m_dist)
#Función principal
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
    listaInv = []

    comm.barrier()
    t_start = MPI.Wtime()

    if pid == 0:
        #R, G, S, I, L, K, M = getValores(argv) #Guardar un valor dado por consola
        data, cant_datos = cargarDatos()
        cant_gusanos = int(cant_datos * 0.9)
        listaInv = generarListaInvertida(data)
        
    
    data,cant_gusanos,listaInv = comm.bcast((data,cant_gusanos,listaInv), root = 0)
    

    inicio = int(pid * cant_gusanos / size)
    final = int(cant_gusanos / size + inicio)
    # print(inicio, " ", final)
    
    for i in range(inicio, final):
        g = Gusano(5.0,randomPos(pid,size))
        g.sacarConjuntoCubierto(1,listaInv,data)
        g.setIntraD(data)
        gusanos.append(g)

        # if len(g.getCCubierto()) != 0:
        #     gusanos.append(g)
        
        

    
    

    gusanos = comm.reduce(gusanos,op = MPI.SUM)
    
    if pid == 0:
        gusanos.sort(key = lambda x: len(x.cCubierto), reverse = True)
    
    t_final = MPI.Wtime()
    tw = comm.reduce(t_final-t_start, op = MPI.MAX)

    if pid == 0:
        print(gusanos[0].getIntraD())
        cont = 0
        for i in gusanos:
            if len(i.cCubierto) > 0:
                #print("Pos = ",str(i.getPos()), "\tIndice = " ,str(i.getCCubierto()), "\tIntraD =", i.getIntraD())
                cont += 1
        print(cont)
        print(tw)

    # if pid == 0:
    #     for i in gusanos:
    #         print(i.getPos())
    #     print(len(gusanos), " ", inicio, " ", final)

if __name__ == "__main__":
    main(sys.argv[1:])