"""
Proyecto I Programación Paralela y Concurrente | CI-0117 | II-Semestre 2020
Profesor: Alan Calderón Castro
Estudiantes: Carlos Espinoza Peraza B92786 y Sebastián Montero Castro B95016

Descripción del proyecto:
    
"""

from mpi4py import MPI
import sys, getopt

#Clase Gusano con X atributos
class Gusano:
    def __init__(self):
        pass

#Se encarga de recibir el valor de los parámetros por consola
def getValores(argv):

    #Atributos que se desean pasar por consola
    r = ""

    try:
        #Se guardan en un tupla la etiqueta(opt) y el valor (arg)
        opts, args = getopt.getopt(argv, "h:r:", ["H=","R="]) #Para agragar parámetros se debe modificar el parámetro "h:r:" -> "h:r:a:b:c:"... y la lista ["H=","R="] -> ["H=","R=","A=","B=","C="]
    except getopt.GetoptError:
        print("Valores incorrectos para la consola")
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == "-h": #Revisa si le pasaron un -h el cual despliega el mensaje de ayuda
            print("Imprimir el -h despliega la ayuda para ver que parámetros recibe por consola")
            sys.exit()
        elif opt in ("-r", "--R"): #Revisa si la etiqueta coincide y guarda el valor en el atributp correspondiente
            r = arg
    
    return int(r) #Retorna el valor para ser usado

#Función principal
def main(argv):
    comm = MPI.COMM_WORLD #Comunicador
    pid = comm.rank       #Proceso
    size = comm.size      #Cantidad de procesos
    R = 0
    if pid == 0:
        R = getValores(argv) #Guardar un valor dado por consola
    
    if pid == 0:
        print(R)
    


if __name__ == "__main__":
    main(sys.argv[1:])