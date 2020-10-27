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
DECREMENTOLUCIFERINA = 0.4
INCREMENTOLUCIFERINA = 0.6

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
    def __init__(self,L,pos,r_s):
        self.nLuciferina = L
        self.pos = pos
        self.posAnterior = pos
        self.vAdaptacion = 0.0
        self.cCubierto = [] #Modificar por un numpy array
        self.vecindario = []
        self.intraD = 0.0
        self.r_s = r_s
        self.F = 0.0
        self.mejorVecino = 0 #indice del mejor vecino en el arreglo vecindario


    def sacarConjuntoCubierto(self,listaInv,datos):
        conjuntoFinal = []
        conjuntoFinal = np.array(conjuntoFinal, dtype = int)
        for i in range(0,10,2):
            conjuntoAux = []
            conjuntoAux = np.array(conjuntoAux, dtype = int)

            minX = math.ceil(self.pos[i] - self.r_s)
            maxX = int(self.pos[i] + self.r_s)
            minY = math.ceil(self.pos[i+1] - self.r_s)
            maxY = int(self.pos[i+1] + self.r_s)

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
            dist = distanciaEuc(self.pos,datos[conjuntoFinal[i]])
            if dist > self.r_s :
                np.delete(conjuntoFinal,i) 

        self.cCubierto = conjuntoFinal
    
    def sacarVecindario(self, gusanos):
        vecindario = []
        for g in gusanos:
            if( (distanciaEuc(self.pos,g.getPos()) < self.r_s) and (self.nLuciferina < g.getNLuciferina()) ):
                vecindario.append(g)
        self.vecindario = vecindario

    def actualizarLuciferina(self):
        luciferina = ((1-DECREMENTOLUCIFERINA) * self.nLuciferina) + (INCREMENTOLUCIFERINA * (self.F))
        self.setNLuciferina(luciferina)

    def moverGusano(self):
        #for i in range(0,10,2):
        return 0

    def getNLuciferina(self):
        return self.nLuciferina

    def getPos(self):
        return self.pos

    def getVAdaptacion(self):
        return self.vAdaptacion
    
    def getCCubierto(self):
        return self.cCubierto
    
    def getVencindario(self):
        return self.vecindario
    
    def getIntraD(self):
        return self.intraD
    
    def getR_s(self):
        return self.r_s

    def getFitness(self):
        return self.F

    def setMejorVecino(self):
        mejorVecinoEncontrado =  -float('inf')
        sumatoriaLuc = 0.0
        for g in range(0,len(self.vecindario)):
            for k in range(0,len(self.vecindario)):
                sumatoriaLuc = sumatoriaLuc + (self.vecindario[k].getNLuciferina() - self.nLuciferina)
            probJ = (self.vecindario[g].getNLuciferina() - self.nLuciferina) / sumatoriaLuc
            if(probJ > mejorVecinoEncontrado):
                self.mejorVecino = g
        return self.vecindario[self.mejorVecino]

    def setFitness(self,n,valor_SSE,maxIntraD):
        self.F = ((1/n) * len(self.cCubierto)) / (valor_SSE * (self.intraD/maxIntraD))

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
        
    def toString(self):
        return "Posiciones = " + str(self.pos) + " | C_r = " + str(self.cCubierto) + " | r_s = " + str(self.r_s) + " | Luciferina = " + str(self.nLuciferina) + " | intraD = " + str(self.intraD)
    
def distanciaEuc(pos1,pos2):
    distancia = 0.0
    for i in range(DIMENSION):
        distancia += math.sqrt(pow((pos1[i] - pos2[i]),2))
    return distancia

"""
def sacarCentroidesCandidatos(diccionario):
    centroidesCandidatos = []
    contador = 1
    while(len(centroidesCandidatos) < 10):
        try:
            centroidesCandidatos.extend(diccionario[len(diccionario)-contador])
            contador = contador + 1
            for i in centroidesCandidatos:
                for j in centroidesCandidatos:
                    if(i != j):
                        print(distanciaEuc(i.getPos(),j.getPos()))
                        if(distanciaEuc(i.getPos(),j.getPos()) <= i.getR_s()):
                            centroidesCandidatos.remove(j)
                            print("Se elimino gusano pues " + str(distanciaEuc(i.getPos(),j.getPos())) + "es menor a 1.5")
        except:
            contador = contador + 1
            
    return centroidesCandidatos
"""
def sacarCentroidesCandidatos(diccionario):
    centroidesCandidatos = diccionario[max(diccionario.keys())]
    return centroidesCandidatos

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
def generarListaInvertida(data, init, final): #[4][13][5]
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
                for l in range(init, final):
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
    #print(contador)
    
def fitness(gusanos):  
    pass

def distIntra(gus):
    m_dist = []
    for i in range(len(gus)):
        d1 = []
        for j in range(len(gus)):
            d1.append(distanciaEuc(gus[i].getPos(),gus[j].getPos()))
        m_dist.append(d1)
    
    #print(m_dist)

def getSSE(centroidesCandidatos,gusanos):
    valor_SSE = 0.0
    for i in centroidesCandidatos:
        for j in gusanos:
            valor_SSE = valor_SSE + distanciaEuc(i.getPos(),j.getPos())
    return valor_SSE

def getInterDist(cc):
    interDist = 0
    for i in range(len(cc)):
        for j in range(len(cc)):
            interDist += distanciaEuc(cc[i].getPos(), cc[j].getPos())
    return interDist

def combinarDiccionarios(dic1,dic2,dataType):
    for i in dic2:
        if(i in dic1):
            dic1[i].extend(dic2[i])
        else:
            dic1[i] = dic2[i]
    return dic1

def combinarListasInvertidas(L1, L2, dataType):
    for i in range(4):
        for j in range(13):
            for k in range(5):
                lista1 = L1[i][j][k]
                lista1.extend(L2[i][j][k])
                L1[i][j][k] = lista1
    return L1

#Función principal
def main(argv):
    comm = MPI.COMM_WORLD       #Comunicador
    pid = comm.rank             #Proceso
    size = comm.size            #Cantidad de procesos

    #Constantes proporcionadas por consola
    R = 0                       #Tasa constante de decremento de luciferina
    G = 0                       #Fracción constante de incremento de luciferina
    S = 0                       #Distancia constante en la que se mueven los gusanos
    I = 0                       #Rango de cobertura de un gusano para incluir datos asociados
    L = 0                       #Valor inicial de luciferina en los gusanos
    K = 0                       #Cantidad de clases a encontrar
    M = 0                       #Tasa de gusanos por dato

    #Variables 
    data = []                   #Conjunto de manos
    cant_gusanos = 0            #Cantidad de gusanos, 90% de la cantidad total de datos
    gusanos = []                #Arreglo de gusanos
    listaInv = []               #Lista invertida con los índices de los datos
    diccionarioC_r = {}         #Key = {cantidad de elementos cubiertos} | Value {Elemenos con 'key' datos cubiertos}
    maxIntraD = 0.0             #Valor maximo de intraD dentro del conjunto de gusanos
    centroidesCandidatos = []   #Lista con los centroides candidatos
    valor_SSE = 0.0             #Valor de la SSE (Squared algo)
    interDist = 0               #Valor de la intradistancia

    #Se sincronizan los procesos
    comm.barrier()              #Función para sincronizar

    #<-----Se inicia la toma del tiempo----->
    t_start = MPI.Wtime()

    """
    Proceso 0 se encarga de recoger los datos pasados por consola, así como cargar los datos
    Realiza el cálculo de la cantidad de Gusanos siendo del 0.9 del total de datos
    """
    if pid == 0:
        #R, G, S, I, L, K, M = getValores(argv) #Guardar un valor dado por consola
        data, cant_datos = cargarDatos()
        
    #Bcast a todos los procesos con la lista de datos
    data = comm.bcast(data, root = 0)

    
    #<------Rangos para la paralelización por tareas------>

    #Se determinan los rangos de trabajo para crear los gusanos
    inicio = int(pid * (len(data)*0.1) / size)
    final = int((len(data)*0.1) / size + inicio)

    #Se determinan los rangos de trabajo para crear la lista invertida
    init_ListaInvertida = int(pid * len(data) / size)
    final_ListaInvertida = int((pid + 1) * len(data) / size)

    #<------Rangos para la paralelización por tareas------>

    #Validación de las funciones reductoras especiales para las diferentes estructuras de datos
    diccionarioSUM = MPI.Op.Create(combinarDiccionarios,commute = True)
    listaInvertidaSUM = MPI.Op.Create(combinarListasInvertidas, commute = True)
    
    #Creación de la lista invertida por procesos
    listaInv = generarListaInvertida(data,init_ListaInvertida, final_ListaInvertida)

    #Se reduce la lista invertida al proceso 0
    listaInv = comm.allreduce(listaInv, op = listaInvertidaSUM)

    #Se realiza un bcast a todos los procesos con la lista invertida
    listaInv = comm.bcast(listaInv, root = 0)

    #Se crean los gusanos dependiendo de la división de trabajo entre procesos
    for i in range(inicio, final): 
        g = Gusano(5.0,randomPos(pid,size),2)
        g.sacarConjuntoCubierto(listaInv,data)
        g.setIntraD(data)
        if(g.getIntraD() > maxIntraD):
            maxIntraD = g.getIntraD()

        if(len(g.getCCubierto()) > 0):                              #Se descartan los gusanos que no cubren ningún dato
            gusanos.append(g)
            if(len(g.getCCubierto()) in diccionarioC_r):            #Se revisa que la cantidad de datos cubiertos esté dentro del diccionario
                diccionarioC_r[len(g.getCCubierto())].append(g)     #Si la cantidad se encuentra se agrega al los value de ese key
            else:
                diccionarioC_r[len(g.getCCubierto())] = [g]         #Si no se encuentra, se crea una nueva key
        
        
    #Se reducen los diccionarios en el proceso 0 
    diccionarioFinalC_r = comm.allreduce(diccionarioC_r, op = diccionarioSUM)
    
    #Se reduce la lista de gusanos al proceso 0
    gusanos = comm.reduce(gusanos,op = MPI.SUM)

    gusanos = comm.bcast(gusanos, root = 0)
    inicio = int(pid * (len(gusanos)*0.9) / size)
    final = int((len(gusanos)*0.9) / size + inicio)

    for i in range(inicio,final):
        gusanos[i].sacarVecindario(gusanos)

    gusanos = comm.reduce(gusanos, op = MPI.SUM)

    
    

    #El procesos 0 se encarga de generar la lista de los centroides cantidatos 
    if pid == 0:
        for i in gusanos:
            print("hola")
            print("Vec: ", i.getVencindario())
        gusanos.sort(key = lambda x: len(x.cCubierto), reverse = True)
        print(diccionarioFinalC_r.keys())
        centroidesCandidatos = sacarCentroidesCandidatos(diccionarioFinalC_r)
        valor_SSE = getSSE(centroidesCandidatos,gusanos)
        interDist = getInterDist(centroidesCandidatos)
    
    #Se hace un bcast a todos los procesos
    centroidesCandidatos, valor_SSE, interDist, maxIntraD = comm.bcast((centroidesCandidatos,valor_SSE,interDist,maxIntraD),0)
    
    
    #while(condiciones): #PARALELIZAR ESTE CICLO TAL QUE ABARQUE SOLO UNA CANTIDAD ESPECIFICA DE GUSANOS
    for i in range(0,1):
        newDiccionarioC_r = {}
        newGusanos = []
        inicio = int(pid * (len(gusanos) / size))
        final = int(len(gusanos) / size + inicio)

        for i in range(inicio, final):
            gusanos[i].setFitness(len(data),valor_SSE,maxIntraD)
            gusanos[i].actualizarLuciferina()
            gusanos[i].sacarVecindario(gusanos) #EXTREMADAMENTE INEFICIENTE, TERMINA TENIENDO UNA COMPLEJIDAD DE TIEMPO n^2 (POSIBLES OPTIMIZACIONES)
            gusanos[i].setMejorVecino()
            gusanos[i].moverGusano()
            gusanos[i].sacarConjuntoCubierto(listaInv,data)
            gusanos[i].setIndraD(data)
            if(len(i.getCCubierto) > 0):
                if(len(gusanos[i].getCCubierto()) in newDiccionarioC_r):
                    newDiccionarioC_r[len(gusanos[i].getCCubierto())].append(i)
                else:
                    newDiccionarioC_r[len(i.getCCubierto())] = [gusanos[i]]
                newGusanos.append(gusanos[i])
            gusanos = newGusanos
            diccionarioFinal = newDiccionarioC_r
            #centroidesCandidatos = SE SACAN LOS CC CON LOS GUSANOS CON F MAS GRANDE
            getSSE(centroidesCandidatos,gusanos)
            getInterDist(centroidesCandidatos)

            #FIN DEL CICLO - ESTE LOOP SE DEBE PARALELIZAR DE TAL MANERA QUE SOLO ITERE CIERTA CANTIDAD DE VECES Y ABARQUE CIERTA CANTIDAD
            #DE GUSANOS, AL FINAL DE CADA ITERACION SE DEBE HACER UN BCAST CON LOS DATOS Y UNIRLOS.
   

    #<-----Se termina la toma del tiempo----->
    t_final = MPI.Wtime()

    #Se reduce la toma del tiempo al proceso 0
    tw = comm.reduce(t_final-t_start, op = MPI.MAX)

    if pid == 0:
        #print(gusanos[0].getIntraD())
        cont = 0
        for i in gusanos:
            if len(i.cCubierto) == 0:
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