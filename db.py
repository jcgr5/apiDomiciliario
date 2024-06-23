import mysql.connector # type: ignore

# Conectar a la base de datos MySql
def crearConexion():
    return mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456',
    database='domiciliarios'
)

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
    
diccionarioNuevoItem = {
    'ID_Domiciliario': 4,
    'Nombre': 'Tom Cruise',
    'UbicacionDomiciliario': '78,9',
    'tarifa': 0.15,
    'FotoDomiciliario': './GestionDB/ImagenesDomiciliario/tom_cruise.jpg',  # Ruta a la foto
    'TipoVehiculo': 'Moto',
    'EstrellasCalificacion': 2
}

id_nuevo_item = adicionarItemAPI(diccionarioNuevoItem)
print(f"ID del nuevo item: {id_nuevo_item}")


