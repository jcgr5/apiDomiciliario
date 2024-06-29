import base64
import mysql.connector
import math
import math
import matplotlib
matplotlib.use('agg')  # Utilizar 'agg' como backend para Matplotlib
import matplotlib.pyplot as plt
import base64
 
#Librerías para la API
import uvicorn
from fastapi import Request, FastAPI, Body, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

import pprint as pp

#Ejecutar el servicio:  python3 -m uvicorn domiciliariosRanking:app --port 8001 --reload --host 127.0.0.1


###-----------FUNCIONES------------###
def crearConexion():
    return mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456',
    database='domiciliarios'
    )


def Ranking():
    try:
        with crearConexion() as conn:
            # Preparar inserción
            sql = f"""
                SELECT ID_Domiciliario, Nombre, TipoVehiculo,EstrellasCalificacion 
                FROM domiciliario
                WHERE EstrellasCalificacion BETWEEN 4 AND 6 
                ORDER BY EstrellasCalificacion desc; 
            """
            cur = conn.cursor()
            cur.execute(sql,None)

            #Guarda los nombres de las columnas de la tabla
            column_names = [i[0] for i in cur.description]
            
            results = cur.fetchall()
            
            #Guarda los resultados de la consulta como tuplas
            consulta = [dict(zip(column_names, row)) for row in results]
            print(consulta)

            Ranking=[]
            for dicts in consulta:
                Ranking.append({
                     'Id': dicts['ID_Domiciliario'],
                     'Nombre': dicts['Nombre'],
                     'TipoVehiculo': dicts['TipoVehiculo'],
                     'EstrellasCalificacion': dicts['EstrellasCalificacion']
                     })
            
                   
            cur.close()

            ###---retorna la "estructura necesaria"---###

            return {
                "Ranking" :Ranking
            }
        
        #return tresMasCercanos
    except mysql.connector.Error as e:
        print(f"Error en la base de datos: {e}")
        return None
    except Exception as e:
        print(f"Error general: {e}")
        return None


#Instanciamos la aplicación
app = FastAPI()

#Activar CORS Middleware
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    #allow_methods=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Permitir estos métodos HTTP
    allow_headers=["*"],
)
app.title = "API de TipoVehiculo"
app.version = "0.0.1"



#Los endpoints de la API entran como decoradores

@app.get("/Rankig")
def RankigDomiciliarios():
	print() 
	resultado = Ranking()
	print(resultado)

	return resultado
     
		

      
    
