import sqlite3
import os
from util import util

class BD:
    def __init__(self):
        self.__dataBase = 'BD/resultados.db'
        self.__conexion = None
        self.__cursor   = None

    def getDataBase(self):
        return self.__dataBase
    def setDataBase(self, dataBase):
        self.__dataBase = dataBase
    def getConexion(self):
        return self.__conexion
    def setConexion(self, conexion):
        self.__conexion = conexion
    def getCursor(self):
        return self.__cursor
    def setCursor(self, cursor):
        self.__cursor = cursor

    def conectar(self):
        conn = sqlite3.connect(self.getDataBase())
        cursor = conn.cursor()
        
        self.setConexion(conn)
        self.setCursor(cursor)
    
    def desconectar(self):
        self.getConexion().close()
        
    def commit(self):
        self.getConexion().commit()
        
    def construirTablas(self):

        self.conectar()
        
        self.getCursor().execute(
            ''' CREATE TABLE IF NOT EXISTS instancias(
                id_instancia INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_problema TEXT,
                nombre TEXT,
                optimo REAL,
                param TEXT
            )'''
        )
        
        self.getCursor().execute(
            ''' CREATE TABLE IF NOT EXISTS experimentos(
                id_experimento INTEGER PRIMARY KEY AUTOINCREMENT,
                MH TEXT,
                paramMH TEXT,
                ML TEXT,
                paramML TEXT,
                ML_FS TEXT,
                paramML_FS TEXT,
                estado TEXT,
                fk_id_instancia INTEGER,
                FOREIGN KEY (fk_id_instancia) REFERENCES instancias (id_instancia)
            )'''
        )

        self.getCursor().execute(
            ''' CREATE TABLE IF NOT EXISTS resultados(
                id_resultado INTEGER PRIMARY KEY AUTOINCREMENT,
                fitness REAL,
                tiempoEjecucion REAL,
                solucion TEXT,
                fk_id_experimento INTEGER,
                FOREIGN KEY (fk_id_experimento) REFERENCES experimentos (id_experimento)
            )'''
        )

        self.getCursor().execute(
            ''' CREATE TABLE IF NOT EXISTS iteraciones(
                id_archivo INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                archivo BLOB,
                fk_id_experimento INTEGER,
                FOREIGN KEY (fk_id_experimento) REFERENCES experimentos (id_experimento)
            )'''
        )
        
        self.commit()
        
        self.insertarInstanciasBEN()
        self.insertarInstanciasFS()
        self.insertarInstanciasSCP()
        
        self.desconectar()
    
    
    def insertarExperimentos(self, data, corridas, id):
        
        self.conectar()

        for corrida in range(corridas):
            self.getCursor().execute(f'''
                INSERT INTO experimentos VALUES (
                    NULL,
                    '{str(data["MH"])}',
                    '{str(data["paramMH"])}',
                    '{str(data["ML"])}',
                    '{str(data["paramML"])}',
                    '{str(data["ML_FS"])}',
                    '{str(data["paramML_FS"])}',
                    '{str(data["estado"])}',
                    {id}
                )''')
        self.commit()
        self.desconectar()
        
    def insertarInstanciasFS(self):
        
        self.conectar()
        
        nombres = ['ionosphere','sonar','Cervical Cancer','Immunotherapy','Divorce','wdbc','breast-cancer-wisconsin']
        for nombre in nombres:
            
            tipoProblema = 'FS'
            optimo = 0
            param = ''
            self.getCursor().execute(f'''  INSERT INTO instancias (tipo_problema, nombre, optimo, param) VALUES(?, ?, ?, ?) ''', (tipoProblema, nombre, optimo, param))
            
        self.commit()
        self.desconectar()
    
    def obtenerExperimento(self):
        
        self.conectar()
        
        cursor = self.getCursor()
        
        cursor.execute(''' SELECT * FROM experimentos WHERE estado = 'pendiente' LIMIT 1 ''')
        data = cursor.fetchall()
        
        self.desconectar()
        
        return data
    
    def obtenerInstancia(self,id):
        
        self.conectar()
        
        cursor = self.getCursor()
        
        cursor.execute(f''' SELECT * FROM instancias WHERE id_instancia = {id} ''')
        data = cursor.fetchall()
        
        self.desconectar()
        
        return data
    
    def actualizarExperimento(self, id, estado):
        
        self.conectar()
        
        cursor = self.getCursor()
        cursor.execute(f''' UPDATE experimentos SET estado = '{estado}' WHERE id_experimento =  {id} ''')
        self.commit()
        self.desconectar()
        
    def insertarIteraciones(self, nombre_archivo, binary, id):
        
        self.conectar()
        
        cursor = self.getCursor()
        cursor.execute(f'''  INSERT INTO iteraciones (nombre, archivo, fk_id_experimento) VALUES(?, ?, ?) ''', (nombre_archivo, binary, id))
        
        self.commit()
        
        self.desconectar()
        
    def insertarResultados(self, BestFitness, tiempoEjecucion, Best, id):
        
        self.conectar()
        
        cursor = self.getCursor()
        
        cursor.execute(f''' INSERT INTO resultados VALUES (
            NULL,
            {BestFitness},
            {round(tiempoEjecucion,3)},
            '{str(Best.tolist())}',
            {id}
        )''')
        
        self.commit()
        
        self.desconectar()
        
    def obtenerArchivos(self, instancia):
        self.conectar()
        
        cursor = self.getCursor()
        cursor.execute(f''' 
            select i.nombre, i.archivo 
            from experimentos e 
            inner join iteraciones i on e.id_experimento  = i.fk_id_experimento 
            inner join instancias i2 on e.fk_id_instancia = i2.id_instancia 
            where i2.nombre  = '{instancia}' 
            order by i2.nombre desc , e.MH desc   
        ''')
        
        data = cursor.fetchall()
        
        
        self.desconectar()
        return data
    
    def obtenerMejoresArchivos(self, instancia, ml):
        self.conectar()
        
        cursor = self.getCursor()
        cursor.execute(f'''             
            select e.id_experimento , e.MH , E.ML, i2.nombre  , i.nombre , i.archivo , MIN(r.fitness)  
            from resultados r 
            inner join experimentos e on r.fk_id_experimento = e.id_experimento
            inner join iteraciones i on i.fk_id_experimento = e.id_experimento
            inner join instancias i2 on e.fk_id_instancia = i2.id_instancia 
            where i2.nombre  = '{instancia}' and e.ML = '{ml}'
            group by e.MH , i2.nombre
                       
        ''')
        
        data = cursor.fetchall()
        
        
        self.desconectar()
        return data
    
    def obtenerMejoresArchivosconClasificador(self, instancia, ml, ml_fs):
        self.conectar()
        
        cursor = self.getCursor()
        cursor.execute(f'''             
            select e.id_experimento , e.MH , E.ML, e.ML_FS, i2.nombre  , i.nombre , i.archivo , MIN(r.fitness) 
            from resultados r 
            inner join experimentos e on r.fk_id_experimento = e.id_experimento
            inner join iteraciones i on i.fk_id_experimento = e.id_experimento
            inner join instancias i2 on e.fk_id_instancia = i2.id_instancia 
            where i2.nombre  = '{instancia}' and e.ML = '{ml}' and e.ML_FS = '{ml_fs}'
            group by e.MH , i2.nombre
                       
        ''')
        
        data = cursor.fetchall()
        
        
        self.desconectar()
        return data
    
    def obtenerMejoresArchivosconBSS(self, instancia, ml, bss):
        self.conectar()
        
        cursor = self.getCursor()
        cursor.execute(f'''             
            select e.id_experimento , e.MH , E.ML, e.ML_FS, i2.nombre  , i.nombre , i.archivo , MIN(r.fitness) 
            from resultados r 
            inner join experimentos e on r.fk_id_experimento = e.id_experimento
            inner join iteraciones i on i.fk_id_experimento = e.id_experimento
            inner join instancias i2 on e.fk_id_instancia = i2.id_instancia 
            where i2.nombre  = '{instancia}' and e.ML = '{ml}' and e.paramMH like '%{bss}%' 
            group by e.MH , i2.nombre
                       
        ''')
        
        data = cursor.fetchall()
        
        
        self.desconectar()
        return data
    
    def obtenerMejoresSoluciones(self, instancia, ml):
        self.conectar()
        
        cursor = self.getCursor()
        cursor.execute(f'''             
            select e.id_experimento , e.MH , E.ML, r.solucion, MIN(r.fitness) 
            from resultados r 
            inner join experimentos e on r.fk_id_experimento = e.id_experimento
            inner join iteraciones i on i.fk_id_experimento = e.id_experimento
            inner join instancias i2 on e.fk_id_instancia = i2.id_instancia 
            where i2.nombre  = '{instancia}' and e.ML = '{ml}'
            group by e.MH , i2.nombre
                       
        ''')
        
        data = cursor.fetchall()
        
        
        self.desconectar()
        return data
    
    
    
    
    
    def obtenerInstancias(self, problema):
        
        self.conectar()
        cursor = self.getCursor()
        cursor.execute(f''' select DISTINCT id_instancia, nombre from instancias i where nombre in ({problema})   ''')
        
        data = cursor.fetchall()
        
        
        self.desconectar()
        return data