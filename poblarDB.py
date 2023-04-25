from BD.sqlite import BD
import json

# mhs = ['SCA','GWO','WOA','PSA']
# pop = 10
# maxIter = 100
# corridas = 1
# funciones de binarizacion: 
#       STD : Estandar
#       COM: Complemento 
#       PS: Probabilidad estática 
#       ELIT: Elitista
# funciones de transferencia: 
#       S-Shape: S1, S2, S3 y S4
#       V-Shape: V1, V2, V3 y V4
#       X-Shape: X1, X2, X3 y X4      
#       Z-Shape: Z1, Z2, Z3 y Z4

# discretizacion = {
#         'combinacion1':['V4','STD']
#     }

bd = BD()


fs  = False
scp = False
ben = False
ml = False
mhs = ['WOA']
cantidad = 0

DS_actions = [
    'V1-STD', 'V1-COM', 'V1-PS', 'V1-ELIT',
    'V2-STD', 'V2-COM', 'V2-PS', 'V2-ELIT',
    'V3-STD', 'V3-COM', 'V3-PS', 'V3-ELIT',
    'V4-STD', 'V4-COM', 'V4-PS', 'V4-ELIT',
    'S1-STD', 'S1-COM', 'S1-PS', 'S1-ELIT',
    'S2-STD', 'S2-COM', 'S2-PS', 'S2-ELIT',
    'S3-STD', 'S3-COM', 'S3-PS', 'S3-ELIT',
    'S4-STD', 'S4-COM', 'S4-PS', 'S4-ELIT',
]

paramsML = json.dumps({
    'MinMax'        : 'min',
    'DS_actions'    : DS_actions,
    'gamma'         : 0.4,
    'policy'        : 'e-greedy',
    'qlAlphaType'   : 'static',
    'rewardType'    : 'withPenalty1',
    'stateQ'        : 2
})


if fs:
    # poblar ejecuciones FS
    instancias = bd.obtenerInstancias(f'''
                                      "sonar"
                                      ''')
    iteraciones = 100
    experimentos = 1
    poblacion = 50
    # clasificadores = ["KNN","RandomForest","Xgboost"]
    clasificadores = ["KNN"]
    for instancia in instancias:

        for mh in mhs:
            for clasificador in clasificadores:
                if ml:
                    data = {}
                    data['MH']          = mh
                    data['paramMH']     = f'iter:{str(iteraciones)},pop:{str(poblacion)}'
                    data['ML']          = 'Q-Learning'
                    data['paramML']     = paramsML
                    data['ML_FS']       = clasificador
                    data['paramML_FS']  = f'k:5'
                    data['estado']      = 'pendiente'

                    cantidad +=experimentos
                    bd.insertarExperimentos(data, experimentos, instancia[0])
                else:
                    data = {}
                    data['MH']          = mh
                    data['paramMH']     = f'iter:{str(iteraciones)},pop:{str(poblacion)},DS:S4-COM'
                    data['ML']          = ''
                    data['paramML']     = ''
                    data['ML_FS']       = clasificador
                    data['paramML_FS']  = f'k:5'
                    data['estado']      = 'pendiente'

                    cantidad +=experimentos
                    bd.insertarExperimentos(data, experimentos, instancia[0])

if scp:
    # poblar ejecuciones SCP
    instancias = bd.obtenerInstancias(f'''
                                      "scp41"
                                      ''')
    iteraciones = 100
    experimentos = 1
    poblacion = 10
    for instancia in instancias:

        for mh in mhs:
            data = {}
            data['MH']          = mh
            data['paramMH']     = f'iter:{str(iteraciones)},pop:{str(poblacion)},DS:V4-ELIT,repair:complex'
            data['ML']          = ''
            data['paramML']     = ''
            data['ML_FS']       = ''
            data['paramML_FS']  = ''
            data['estado']      = 'pendiente'

            cantidad +=experimentos
            bd.insertarExperimentos(data, experimentos, instancia[0])
            
if ben:
    # poblar ejecuciones Benchmark
    instancias = bd.obtenerInstancias(f'''
                                      "F7","F8","F9","F10"
                                      ''')
    iteraciones = 500
    experimentos = 31
    poblacion = 30
    for instancia in instancias:
        for mh in mhs:
            data = {}
            data['MH']          = mh
            data['paramMH']     = f'iter:{str(iteraciones)},pop:{str(poblacion)}'
            data['ML']          = ''
            data['paramML']     = ''
            data['ML_FS']       = ''
            data['paramML_FS']  = ''
            data['estado']      = 'pendiente'

            cantidad +=experimentos
            bd.insertarExperimentos(data, experimentos, instancia[0])

print("------------------------------------------------------------------")
print(f'Se ingresaron {cantidad} experimentos a la base de datos')
print("------------------------------------------------------------------")

