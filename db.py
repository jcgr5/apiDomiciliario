import mysql.connector
import sys
import json
import math

#----------------------------------FUNCIONES---------------------------------------------------
# Conectar a la base de datos MySql
def crearConexion():
    return mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456',
    database='domiciliarios'
)

#ditancia euclidiana
def distaciaEu(coor1,coor2):
    x1,y1 = coor1
    x2,y2 = coor2
    distancia = math.sqrt((float(x2) - float(x1)) ** 2 + (float(y2) - float(y1)) ** 2)
    return int(distancia)

#Insertar sql
def adicionarItemAPI(diccionarioNuevoItem):
    # Convertir datos digitales (foto) en formato binario para la base de datos
    fotoFormatoBlob = None  #variable que recibirá la foto
    try:
        with open(diccionarioNuevoItem['FotoDomiciliario'], 'rb') as archivoFoto:
            fotoFormatoBlob = archivoFoto.read()
    except FileNotFoundError:
        print(f"No se encontró el archivo: {diccionarioNuevoItem['FotoDomiciliario']}")
        return None
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None
     # Instanciar la conexión y realizar la consulta mientras está abierta
    try:
        with crearConexion() as conn:
            # Preparar inserción
            sql = """
                INSERT INTO domiciliario 
                (ID_Domiciliario, Nombre, UbicacionDomiciliario, tarifa, FotoDomiciliario, TipoVehiculo, EstrellasCalificacion) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cur = conn.cursor()
            cur.execute(sql, (
                diccionarioNuevoItem['ID_Domiciliario'],
                diccionarioNuevoItem['Nombre'],
                diccionarioNuevoItem['UbicacionDomiciliario'],
                diccionarioNuevoItem['tarifa'],
                fotoFormatoBlob,
                diccionarioNuevoItem['TipoVehiculo'],
                diccionarioNuevoItem['EstrellasCalificacion']
            ))
            conn.commit()
            conn.close() 
            return cur.lastrowid
    except mysql.connector.Error as e:
        print(f"Error en la base de datos: {e}")
        return None
    except Exception as e:
        print(f"Error general: {e}")
        return None

#Hallar domiciliario mas cercano
def masCercano(coorCliente1,coorcliente2):
    try:
        with crearConexion() as conn:
            # Preparar inserción
            sql = """
                SELECT Id_Domiciliario, Nombre, UbicacionDomiciliario 
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
                coordenadas.append((float(x),float(y)))
           
            #Calcula la ubicaion mas cercana al cliente
            minDist = sys.maxsize
            ubiMasCerc = () 
            coorCliente = (coorCliente1,coorcliente2)
            for ubi in coordenadas:
                    distancia = distaciaEu(ubi,coorCliente)
                    if distancia<minDist:
                        minDist=distancia
                        ubiMasCerc=ubi
            cont=0
            for i in coordenadas:
                cont+=1
                if ubiMasCerc == i:
                    break
            cur.close() 
            return json.dumps(results[cont-1])
    except mysql.connector.Error as e:
        print(f"Error en la base de datos: {e}")
        return None
    except Exception as e:
        print(f"Error general: {e}")
        return None

#Consultar conductores por tipode vehiculo
def consultarVehiculo():
    try:
        with crearConexion() as conn:
            # Preparar inserción
            sql = """
                SELECT Nombre, TipoVehiculo 
                FROM domiciliario 
                ORDER BY TipoVehiculo
            """
            cur = conn.cursor()
            cur.execute(sql,None)
            consulta = cur.fetchall()
            cur.close() 
            return json.dumps(consulta)
    except mysql.connector.Error as e:
        print(f"Error en la base de datos: {e}")
        return None
    except Exception as e:
        print(f"Error general: {e}")
        return None

#Consultar Ranking de estrellas
def rankingEstrellas():
    try:
        with crearConexion() as conn:
            # Preparar inserción
            sql = """
                SELECT Nombre, EstrellasCalificacion 
                FROM domiciliario 
                ORDER BY EstrellasCalificacion desc
            """
            cur = conn.cursor()
            cur.execute(sql,None)
            consulta = cur.fetchall()
            cur.close() 
            return json.dumps(consulta)
    except mysql.connector.Error as e:
        print(f"Error en la base de datos: {e}")
        return None
    except Exception as e:
        print(f"Error general: {e}")
        return None


#----------------------------------FIN FUNCIONES-----------------------------------------------
if len(sys.argv) > 1:
    param = sys.argv[1]
    if param == "1":
        print(masCercano(float(sys.argv[2]),float(sys.argv[3])))
    elif param == "2":
        print(consultarVehiculo())
    elif param == "3":
        print(rankingEstrellas())
else:
    print("No se recibio ningun parametro")


diccionarioNuevoItem = {
    'ID_Domiciliario': 4,
    'Nombre': 'Tom Cruise',
    'UbicacionDomiciliario': '78,9',
    'tarifa': 0.15,
    'FotoDomiciliario': './GestionDB/ImagenesDomiciliario/tom_cruise.jpg',  # Ruta a la foto
    'TipoVehiculo': 'Moto',
    'EstrellasCalificacion': 2
}

#id_nuevo_item = adicionarItemAPI(diccionarioNuevoItem)
#print(f"ID del nuevo item: {id_nuevo_item}")


