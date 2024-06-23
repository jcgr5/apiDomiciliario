package main

import (
	"net/http"

	"github.com/gorilla/mux"
	"github.com/jcgr5/apiDomiciliario/handlers"
)

func main() {
	router := mux.NewRouter()

	//Definicion de las rutas
	//3 domiciliarios mas cercanos a la ruta indicada
	router.HandleFunc("/domiciliario/masCercano", handlers.MasCercano).Methods("POST")

	//Domiciliarios por tipo de vehiculo
	router.HandleFunc("/domiciliario/tipoVehiculo", handlers.TipoVehiculo).Methods("POST")

	//Ranking calificacion
	router.HandleFunc("/domiciliario/ranking", handlers.Ranking).Methods("POST")

	//iniciar servidor
	http.ListenAndServe(":8080", router)
}
