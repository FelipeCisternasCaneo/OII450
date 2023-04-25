from Problem.FS.Problem import FeatureSelection
import numpy as np


fs = True
empatia = False

fitness = 0
accuracy = 0
f1score = 0
precision = 0
recall = 0
mcc = 0
errorRate = 0
totalFeatureSelected = 0


    
if fs:
    instancias = ['ionosphere','sonar','Immunotherapy','Divorce','wdbc','breast-cancer-wisconsin']
    
    clasificadores = ['KNN','RandomForest','Xgboost']
    
    for archivo in instancias:
    
        print("---------------------------------------------------------")
        instancia = FeatureSelection(archivo)
        print("---------------------------------------------------------")
        # print(len(instancia.getDatos().columns))

        individuo = np.ones(instancia.getTotalFeature())
        # individuo = np.array([0,1,1,0,1,1,1,0,0,0,0 ,1 ,0 ,1 ,1 ,1 ,1 ,1 ,1 ,0 ,1 ,0 ,0 ,0 ,0 ,1 ,0 ,0 ,1 ,1 ,1 ,0 ,1 ,0 ,1 ,1 ,0 ,0 ,1 ,0 ,1 ,1 ,0 ,0 ,0 ,1 ,1 ,1 ,0 ,1 ,0 ,1 ,0 ,1 ,1 ,1 ,0 ,1 ,1 ,0 ,1 ,0 ,0 ])
        # [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62]
        # [0,1,1,0,1,1,1,0,0,0,0 ,1 ,0 ,1 ,1 ,1 ,1 ,1 ,1 ,0 ,1 ,0 ,0 ,0 ,0 ,1 ,0 ,0 ,1 ,1 ,1 ,0 ,1 ,0 ,1 ,1 ,0 ,0 ,1 ,0 ,1 ,1 ,0 ,0 ,0 ,1 ,1 ,1 ,0 ,1 ,0 ,1 ,0 ,1 ,1 ,1 ,0 ,1 ,1 ,0 ,1 ,0 ,0 ]
        # individuo = np.random.randint(low=0, high=2, size = (len(instancia.getDatos().columns)))
        
        seleccion = np.where(individuo == 1)[0]
        # print(individuo)
        # print(seleccion)

        for clasificador in clasificadores:
        
            fitness, accuracy, f1score, precision, recall, mcc, errorRate, totalFeatureSelected = instancia.fitness(seleccion, clasificador, "k:5")

            print(
                f'--------------------------------------------\n'+
                f'clasificador            : {clasificador}\n'+
                f'fitness                 : {str(fitness)}\n'+
                f'accuracy                : {str(accuracy)}\n'+
                f'f-score                 : {str(f1score)}\n'+
                f'precision               : {str(precision)}\n'+
                f'recall                  : {str(recall)}\n'+
                f'mcc                     : {str(mcc)}\n'+
                f'errorRate               : {str(errorRate)}\n'+
                f'total Feature Selected  : {str(totalFeatureSelected)}\n'+
                f'--------------------------------------------')