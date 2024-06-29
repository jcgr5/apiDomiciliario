package servicio

import (
	"net/http"

	"github.com/gorilla/mux"
	"github.com/jcgr5/apiDomiciliario/handlers"
)

func Servicio() {
	router := mux.NewRouter()

	//Definicion de las rutas

	//Domiciliarios por tipo de vehiculo
	router.HandleFunc("/TipoVehiculo", handlers.TipoVehiculo)

	//iniciar servidor
	http.ListenAndServe("0.0.0.0:8081", router)
}
