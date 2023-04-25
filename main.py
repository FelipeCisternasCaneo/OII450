from Solver.solverFS import solverFS
from Solver.solverFSML import solverFSML
from BD.sqlite import BD
import json
# problems = ['ionosphere.data']
bd = BD()

data = bd.obtenerExperimento()

id              = 0
instancia       = ''
problema        = ''
mh              = ''
parametrosMH    = ''
maxIter         = 0
pop             = 0
ds              = []
clasificador    = ''
parametrosC     = '' 

pruebas = 1
while len(data) > 0: 
# while pruebas == 1:
    print("-------------------------------------------------------------------------------------------------------")
    print(data)
    
    id = int(data[0][0])
    id_instancia = int(data[0][8])
    datosInstancia = bd.obtenerInstancia(id_instancia)
    print(datosInstancia)
    
    problema = datosInstancia[0][1]
    instancia = datosInstancia[0][2]
    parametrosInstancia = datosInstancia[0][4]
    mh = data[0][1]
    parametrosMH = data[0][2]
    ml = data[0][3]

    
    maxIter = int(parametrosMH.split(",")[0].split(":")[1])
    pop = int(parametrosMH.split(",")[1].split(":")[1])
    ds = []
    
    if problema == 'FS':
        bd.actualizarExperimento(id, 'ejecutando')
        
        if len(ml) > 1:
            parametrosML = json.loads(data[0][4])
            clasificador = data[0][5]
            parametrosC = data[0][6]
            solverFSML(id, mh, maxIter, pop, instancia, clasificador, parametrosC, parametrosML, ml)
        else:
            
            ds.append(parametrosMH.split(",")[2].split(":")[1].split("-")[0])
            ds.append(parametrosMH.split(",")[2].split(":")[1].split("-")[1])
            
            clasificador = data[0][5]
            parametrosC = data[0][6]
            solverFS(id, mh, maxIter, pop, instancia, ds, clasificador, parametrosC)
        
    data = bd.obtenerExperimento()
    
    
    pruebas += 1
    
print("-------------------------------------------------------")
print("-------------------------------------------------------")
print("Se han ejecutado todos los experimentos pendientes.")
print("-------------------------------------------------------")
print("-------------------------------------------------------")

