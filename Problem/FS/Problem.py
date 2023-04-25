import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from MachineLearning.KNN import KNN
from MachineLearning.RandomForest import RandomForest
from MachineLearning.Xgboost import Xgboost

class FeatureSelection:
    def __init__(self, instance):
        self.__datos = None
        self.__clases = None
        self.__trainingData = None
        self.__trainingClass = None
        self.__testingData = None
        self.__testingClass = None
        self.__gamma = 0.99
        self.__totalFeature = None
        self.readInstance(instance)

    def setDatos(self, datos):
        self.__datos = datos
    def getDatos(self):
        return self.__datos
    def setClases(self, clases):
        self.__clases = clases
    def getClases(self):
        return self.__clases
    def setTrainingData(self, trainingData):
        self.__trainingData = trainingData
    def getTrainingData(self):
        return self.__trainingData
    def setTrainingClass(self, trainingClass):
        self.__trainingData = trainingClass
    def getTrainingClass(self):
        return self.__trainingClass
    def setTestingData(self, testingData):
        self.__testingData = testingData
    def getTestingData(self):
        return self.__testingData
    def setTestingClass(self, testingClass):
        self.__testingClass = testingClass
    def getTestingClass(self):
        return self.__testingClass
    def setGamma(self, gamma):
        self.__gamma = gamma
    def getGamma(self):
        return self.__gamma
    def setTotalFeature(self, totalFeature):
        self.__totalFeature = totalFeature
    def getTotalFeature(self):
        return self.__totalFeature

    def readInstance(self, instance):        
        print(instance)
        if instance == 'ionosphere':
            instance = instance+".data"
            classPosition = 34
            dataset = pd.read_csv('Problem/FS/Instances/'+instance, header=None)
            clases = dataset.iloc[:,classPosition]
            clases = clases.replace({
                'b':0,
                'g':1
            })
            clases = clases.values

            datos = dataset.drop(dataset.columns[classPosition],axis='columns')
            
               
        if instance == 'sonar':
            instance = instance+".all-data"
            classPosition = 60
            dataset = pd.read_csv('Problem/FS/Instances/'+instance, header=None)
            clases = dataset.iloc[:,classPosition]
            clases = clases.replace({
                'R':0,
                'M':1
            })
            clases = clases.values

            datos = dataset.drop(dataset.columns[classPosition],axis='columns')
            
        if instance == 'Immunotherapy':
            instance = instance+".csv"
            classPosition = 7
            dataset = pd.read_csv('Problem/FS/Instances/'+instance, header=None)
            clases = dataset.iloc[:,classPosition]
            clases = clases.values

            datos = dataset.drop(dataset.columns[classPosition],axis='columns')
            
        if instance == 'Divorce':
            instance = "divorce.csv"
            classPosition = 54
            dataset = pd.read_csv('Problem/FS/Instances/'+instance, header=None)
            clases = dataset.iloc[:,classPosition]
            clases = clases.values

            datos = dataset.drop(dataset.columns[classPosition],axis='columns')
            
            
        if instance == 'Hill-Valley-with-noise.data' or instance == 'Hill-Valley-without-noise.data':
            classPosition = 100
            dataset = pd.read_csv('Problem/FS/Instances/'+instance, header=None)
            clases = dataset.iloc[:,classPosition]
            clases = clases.values

            datos = dataset.drop(dataset.columns[classPosition],axis='columns')
        
        # posee datos nulos (?)
        
        if instance == 'breast-cancer-wisconsin':
            instance = instance+".data"
            classPosition = 10
            dataset = pd.read_csv('Problem/FS/Instances/'+instance, header=None)
            clases = dataset.iloc[:,classPosition]
            clases = clases.replace({
                2:0,
                4:1
            })
            clases = clases.values

            datos = dataset.drop(dataset.columns[classPosition],axis='columns')
        
        if instance == 'wdbc':
            instance = instance+".data"
            classPosition = 1
            dataset = pd.read_csv('Problem/FS/Instances/'+instance, header=None)
            clases = dataset.iloc[:,classPosition]
            clases = clases.replace({
                'M':0,
                'B':1
            })
            clases = clases.values

            datos = dataset.drop(dataset.columns[classPosition],axis='columns')

        self.setClases(clases)
        self.setDatos(datos)
        self.setTotalFeature(len(datos.columns))

    def selection(self, seleccion):

        datos = self.getDatos().iloc[:, seleccion]

        escalador = preprocessing.MinMaxScaler()
        # escalador = preprocessing.StandardScaler()

        train_ratio = 0.8
        test_ratio = 0.2
        SEED = 12
        
        trainingData, testingData, trainingClass, testingClass  = train_test_split(
            datos,
            self.getClases(),
            test_size= 1 - train_ratio,
            random_state=SEED,
            stratify=self.getClases()
        )

        trainingData = escalador.fit_transform(trainingData)
        testingData = escalador.fit_transform(testingData)

        return trainingData, testingData, trainingClass, testingClass

    def fitness(self, individuo, clasificador, parametrosC):
        accuracy = 0 
        f1Score = 0
        presicion = 0
        recall = 0
        mcc = 0
        trainingData, testingData, trainingClass, testingClass = self.selection(individuo)
        # cm, accuracy, f1Score, presicion, recall, mcc = self.KNN(trainingData, testingData, trainingClass, testingClass)

        if clasificador == 'KNN':
            accuracy, f1Score, presicion, recall, mcc = KNN(trainingData, testingData, trainingClass, testingClass, int(parametrosC.split(":")[1]))
        if clasificador == 'RandomForest':
            accuracy, f1Score, presicion, recall, mcc = RandomForest(trainingData, testingData, trainingClass, testingClass)
        
        if clasificador == 'Xgboost':
            accuracy, f1Score, presicion, recall, mcc = Xgboost(trainingData, testingData, trainingClass, testingClass)
            
        errorRate = np.round((1 - accuracy), decimals=3)

        fitness = np.round(( self.getGamma() * errorRate ) + ( ( 1 - self.getGamma() ) * ( len(individuo) / self.getTotalFeature() ) ), decimals=3)

        # return fitness, cm, accuracy, f1Score, presicion, recall, mcc, errorRate
        return fitness, accuracy, f1Score, presicion, recall, mcc, errorRate, len(individuo)

    def factibilidad(self, individuo):
        suma = np.sum(individuo)
        if suma > 0:
            return True
        else:
            return False

    def nuevaSolucion(self):
        return np.random.randint(low=0, high=2, size = self.getTotalFeature())
