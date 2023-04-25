El archivo "crearBD.py" crea las tablas en la base de datos

En primer lugar deben poblar la base de datos con experimentos para poder ejecutarlos.

En el archivo "poblarDB.py" pueden realizar este paso. Podrán elegir lo siguiente:
    instancia ejecutar (dataset a filtrar)
    esquema de binarización a aplicar
    metaheurística a utilizar
    numero de iteraciones a ejecutar
    tamaño de la población 

Una vez cargada la información a la bases de datos, deben ejecutar el archivo "main.py"
Este archivo trae un experimento de la base de datos y lo ejecutado

Ustedes deben incorporar su metaheuristica ("suMH.py") en la carpeta "Metaheuristics" y importarlo en el archivo "solverFS.py"

