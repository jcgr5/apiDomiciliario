package DBgo

import (
	"database/sql"
	"fmt"

	_ "github.com/go-sql-driver/mysql"
)

type Domiciliario struct {
	ID                    int
	Nombre                string
	UbicacionDomiciliario string
	Tarifa                float64
	TipoVehiculo          string
	EstrellasCalificacion int
}

func Conexion(tipo string) ([]Domiciliario, error) {

	// Configuración de la conexión
	dsn := "root:123456@tcp(127.0.0.1:3306)/domiciliarios"

	// Establecer la conexión
	db, err := sql.Open("mysql", dsn)
	if err != nil {
		return nil, fmt.Errorf("error al abrir la base de datos: %v", err)
	}
	defer db.Close()

	err = db.Ping()
	if err != nil {
		return nil, fmt.Errorf("error al conectar con la base de datos: %v", err)
	}
	fmt.Println("Conexión exitosa a la base de datos")

	domiciliarios, err := obtenerDomiciliarios(db, tipo)
	if err != nil {
		return nil, fmt.Errorf("error al obtener domiciliarios: %v", err)
	}

	return domiciliarios, nil

}

func obtenerDomiciliarios(db *sql.DB, tipo string) ([]Domiciliario, error) {
	//query := "SELECT id_Domiciliario, Nombre, UbicacionDomiciliario,Tarifa,TipoVehiculo, EstrellasCalificacion FROM domiciliarios"
	query := "SELECT id_Domiciliario, Nombre, UbicacionDomiciliario,Tarifa,TipoVehiculo, EstrellasCalificacion FROM domiciliario WHERE TipoVehiculo = ?"
	rows, err := db.Query(query, tipo)
	if err != nil {
		return nil, fmt.Errorf("error al consultar domiciliarios: %v", err)
	}
	defer rows.Close()

	var domiciliarios []Domiciliario
	for rows.Next() {
		var d Domiciliario
		err := rows.Scan(&d.ID, &d.Nombre, &d.UbicacionDomiciliario, &d.Tarifa, &d.TipoVehiculo, &d.EstrellasCalificacion)
		if err != nil {
			return nil, fmt.Errorf("error al escanear la fila: %v", err)
		}
		domiciliarios = append(domiciliarios, d)
	}
	return domiciliarios, nil
}
