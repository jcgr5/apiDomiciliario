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

#Ejecutar el servicio:  python3 -m uvicorn apiEstudiantes:app --port 8000 --reload --host 127.0.0.1

def crearConexion():
    return mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456',
    database='domiciliarios'
)

def hallarMenor(lista,tresCercanos):
    # Encontrar la clave con la menor distancia
    min_element = min(lista, key=lambda x: x['distancia'])
    
    # Crear un nuevo diccionario con el elemento con la menor distancia
    tresCercanos.append(min_element)
    
    # Eliminar el elemento del diccionario original
    lista.remove(min_element)
    return lista

def distaciaEu(coor1,coor2,coorCliente):
    x1,y1 = coor1,coor2
    x2,y2 = coorCliente
    distancia = math.sqrt((float(x2) - float(x1)) ** 2 + (float(y2) - float(y1)) ** 2)
    return float(distancia)

def masCercano(coorCliente1,coorCliente2):
    try:
        with crearConexion() as conn:
            # Preparar inserción
            sql = """
                SELECT Id_Domiciliario,Nombre,UbicacionDomiciliario 
                FROM domiciliario 
            """
            cur = conn.cursor()
            cur.execute(sql,None)

            #Guarda los nombres de las columnas de la tabla
            column_names = [i[0] for i in cur.description]
            
            results = cur.fetchall()
            
            #Guarda los resultados de la consulta como tuplas
            consulta = [dict(zip(column_names, row)) for row in results]

            coordenadas=[]
            
            #recorre el resultado de la consulta SQL y obtine las coordenadas
            for dicts in consulta:
                coorStr=dicts['UbicacionDomiciliario']
                x,y = coorStr.split(',')
                coordenadas.append({
                     'id': dicts['Id_Domiciliario'],
                     'Nombre': dicts['Nombre'],
                     'X':float(x),
                     'Y':float(y)
                     })
            #print("diccionario con coordenadas de la consulta",coordenadas)    
           
            #Calcula la ubicaion mas cercana al cliente
            distancias = [] 
            coorCliente = (float(coorCliente1),float(coorCliente2))
            for ubi in coordenadas:
                    distancia = distaciaEu(ubi['X'],ubi['Y'],coorCliente)
                    distancias.append({
                         'id':ubi['id'],
                         'Nombre': ubi['Nombre'],
                         'X':ubi['X'],
                         'Y':ubi['Y'],
                         'distancia': distancia
                    })
            #print("diccionario con distancias",distancias)
            tresMasCercanos=[]
            for i in range(3):
                distancias= hallarMenor(distancias,tresMasCercanos)
            #print("\n vector con los 3 mas cercanos",tresMasCercanos)    
            cur.close()


        #--------------- Crear el gráfico-----------------------------------------------------
            fig,ax = plt.subplots(figsize=(10,6))
            
            ###--------imprimir los domiciliarios mas cercanos en verde----------###
            for item in tresMasCercanos:
                ax.scatter(item['X'], item['Y'], color='green')
                ax.text(item['X'], item['Y'], f" ID: {item['id']}", fontsize=9, color='green')
  
            ###--------imprimir el resto de domiciliarios en rojo----------###
            for item in distancias:
                ax.scatter(item['X'], item['Y'], color='red')
                ax.text(item['X'], item['Y'], f" ID: {item['id']}", fontsize=9, color='red')

            ###--------imprimir el cliente en azul----------###
            ax.scatter(coorCliente[0], coorCliente[1], color='blue')
            ax.text(coorCliente[0], coorCliente[1], " Cliente", fontsize=9, color='blue')

            ###---guarda la imagen, cierra plt y codifica la imagen en base64---###
            plt.savefig('mas_cercanos.png')
            plt.close()
            with open('mas_cercanos.png', mode="rb") as file:
                imagenCodificada = base64.b64encode(file.read()).decode('utf-8')
         #---------------Fin Crear el gráfico-----------------------------------------------------
            
            ###---retorna la "estructura necesaria"---###
            ###--Nota: la estructura que recibe debe llevar estos mismo nombres--###
            return {
                "nombreArchivo": "mas_cercanos.png",
                "contenidoArchivo": imagenCodificada,
                "masCercanos": tresMasCercanos
            }
        
        #return tresMasCercanos
    except mysql.connector.Error as e:
        print(f"Error en la base de datos: {e}")
        return None
    except Exception as e:
        print(f"Error general: {e}")
        return None




#Funciones adicionales
def eliminarVocales(nombre):
	nuevaCadena = str()
	for letra in nombre:
		if letra.lower() in "aeiou":
			nuevaCadena += "_"
		else:
			nuevaCadena += letra
	return nuevaCadena

#Simular base de datos de estudiantes
bd = [
    {'id':234, 'nombre':'Hugo', 'idNota':7},
    {'id':123, 'nombre':'Paco', 'idNota':9},
    {'id':777, 'nombre':'Luis', 'idNota':11}
]

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
app.title = "API de Estudiantes"
app.version = "0.0.1"



#Los endpoints de la API entran como decoradores

@app.get("/domiciliarioMasCercano")
def obtenerMasCercanos(coorCliente1:str,coorCliente2:str):
    
	print()
	print(coorCliente1,coorCliente2)  
	resultado = masCercano(coorCliente1,coorCliente2)
	print(resultado)

	return resultado
     

def construir():
	import matplotlib
	matplotlib.use('agg')  
	import matplotlib.pyplot as plt  
	

	plt.scatter(iris['sepal_length'], iris['sepal_width'])
	plt.savefig('iris.png')
	file = open('iris.png', mode="rb")

	imagenCodificada = base64.b64encode(file.read())
	
	file.close()

	return {
				"nombreArchivo" : "iris.png",
				"contenidoArchivo": imagenCodificada,
					
			}  
		

@app.get("/plot-iris")
def plot_iris():    
    
    return construir()
      
    
    
