import math
import os
import random
def esDecimal(numero):
    try:
        float(numero)
        return True
    except:
        return False

def distEuclidiana(x, y, missd, missdValue):
    suma = 0
    for i in range(x.__len__()):
        if missd:
            if x[i] != missdValue and y[i] != missdValue:
                suma = suma + ( (x[i] - y[i])**2 )
        else:
            suma = suma + ((x[i] - y[i]) ** 2)
    return math.sqrt(suma)

def porcentajesXLPXPT(div, maxDiv):
    XPL = round((div/maxDiv)*100,2)
    XPT = round((abs(div-maxDiv)/maxDiv)*100,2)
    state = -1
    #Determinar estado
    if XPL >= XPT:
        state = 1 # Exploración
    else:
        state = 0 # Explotación
    return XPL, XPT, state

def diversidadHussain(matriz):
    # [ [1,2,3,4,5,6],
    #   [6,5,4,3,2,1],
    #   [1,2,3,4,5,6],
    #   [6,5,4,3,2,1],
    #   [1,2,3,4,5,6],
    #   [6,5,4,3,2,1],
    #   [1,2,3,4,5,6] ]
    medianas = []
    for j in range(matriz[0].__len__()):
        suma = 0
        for i in range(matriz.__len__()):
            suma += matriz[i][j]
        medianas.append(suma/matriz.__len__())
    n = len(matriz)
    l = len(matriz[0])
    diversidad = 0
    for d in range(l):
        div_d = 0
        for i in range(n):
            div_d = div_d + abs(medianas[d] - matriz[i][d])
        diversidad = diversidad + div_d
    return (1 / (l*n)) * diversidad

def selectionSort(lista):
    posiciones = []
    for i in range(len(lista)):
        posiciones.append(i) 
    for i in range(len(lista)):
        lowest_value_index = i
        for j in range(i + 1, len(lista)):
            if lista[j] < lista[lowest_value_index]:
                lowest_value_index = j
        lista[i], lista[lowest_value_index] = lista[lowest_value_index], lista[i]
        posiciones[i], posiciones[lowest_value_index] = posiciones[lowest_value_index], posiciones[i]
    return posiciones

def normr(Mat):
    norma = 0
    for i in range(Mat.__len__()):
        norma = norma + abs(math.pow(Mat[i],2))
    norma = math.sqrt(norma)
    B = []
    for i in range(Mat.__len__()):
        B.append(Mat[i]/norma)
    return B

def getUbLb(poblacion, dimension):
    ub = []
    lb = []
    for j in range(dimension):
        lista = []
        for i in range(poblacion.__len__()):
            lista.append(poblacion[i][j])
        ordenLista = selectionSort(lista)
        ub.append(poblacion[ordenLista[poblacion.__len__()-1]][j])
        lb.append(poblacion[ordenLista[0]][j])    
    return ub, lb

def RouletteWheelSelection(weights):
    accumulation = sum(weights)
    p = random.random() * accumulation
    chosen_index = -1
    suma = 0
    for index in range(len(weights)):
        suma = suma + weights[index]
        if suma > p:
            chosen_index = index
            break
    choice = chosen_index
    return choice

# Create a function that converts a digital file into binary
def convert_into_binary(file_path):
    with open(file_path, 'rb') as file:
        binary = file.read()

    return binary

def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)