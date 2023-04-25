import pandas as pd
from BD.sqlite import BD
import numpy as np


bd = BD()

instance = "nefrologia.csv"
classPosition = 62
dataset = pd.read_csv('Problem/FS/Instances/'+instance)
dataset = dataset.drop(['Sex','Diabetes','H0_Bano','H0_Dializador','Hypo_Type','TAS_Diff','Hypo_Type2'], axis=1)
clases = dataset.iloc[:,classPosition]
clases = clases.values

datos = dataset.drop(dataset.columns[classPosition], axis='columns')

column_names = list(datos.columns)

print("-----------------------------------------------------------------------------------------------------------------------")
print(column_names)
print("-----------------------------------------------------------------------------------------------------------------------")

mejores = bd.obtenerMejoresSoluciones('nefrologia','')


seleccionGWO = []
seleccionMFO = []
seleccionPSA = []
seleccionSCA = []
seleccionWOA = []


for data in mejores:
    caracteristicas = []
    mh = data[1]
    solucion = data[3].replace("[","").replace("]","").replace("0.0",str(0)).replace("1.0",str(1)).split(",")
    print(mh)
    i = 0
    for feature in solucion:
        
        if int(feature) == 1:
            caracteristicas.append(column_names[i])
            if mh == 'GWO':
                seleccionGWO.append(i)
            
            if mh == 'MFO':
                seleccionMFO.append(i)
                
            if mh == 'PSA':
                seleccionPSA.append(i)
                
            if mh == 'SCA':
                seleccionSCA.append(i)
                
            if mh == 'WOA':
                seleccionWOA.append(i)
        
        i+=1
    print(caracteristicas)
print("-----------------------------------------------------------------------------------------------------------------------")
print(seleccionGWO)
print(len(seleccionGWO))
print("-----------------------------------------------------------------------------------------------------------------------")
print(seleccionMFO)
print(len(seleccionMFO))
print("-----------------------------------------------------------------------------------------------------------------------")
print(seleccionPSA)
print(len(seleccionPSA))
print("-----------------------------------------------------------------------------------------------------------------------")
print(seleccionSCA)
print(len(seleccionSCA))
print("-----------------------------------------------------------------------------------------------------------------------")
print(seleccionWOA)
print(len(seleccionWOA))
print("-----------------------------------------------------------------------------------------------------------------------")

diccionario = {}

for caracteristica in seleccionGWO:
    if column_names[caracteristica] in diccionario:
        diccionario[column_names[caracteristica]] =  diccionario[column_names[caracteristica]] + 1
    else:
        diccionario[column_names[caracteristica]] = 1
        
for caracteristica in seleccionMFO:
    if column_names[caracteristica] in diccionario:
        diccionario[column_names[caracteristica]] =  diccionario[column_names[caracteristica]] + 1
    else:
        diccionario[column_names[caracteristica]] = 1

for caracteristica in seleccionPSA:
    if column_names[caracteristica] in diccionario:
        diccionario[column_names[caracteristica]] =  diccionario[column_names[caracteristica]] + 1
    else:
        diccionario[column_names[caracteristica]] = 1

for caracteristica in seleccionSCA:
    if column_names[caracteristica] in diccionario:
        diccionario[column_names[caracteristica]] =  diccionario[column_names[caracteristica]] + 1
    else:
        diccionario[column_names[caracteristica]] = 1

for caracteristica in seleccionWOA:
    if column_names[caracteristica] in diccionario:
        diccionario[column_names[caracteristica]] =  diccionario[column_names[caracteristica]] + 1
    else:
        diccionario[column_names[caracteristica]] = 1


import operator

diccionarionOrdenado = sorted(diccionario.items(), key=operator.itemgetter(1), reverse=True)

# print(diccionarionOrdenado)

for campo in diccionarionOrdenado:
    print(campo)