package ServicioIntermediario

import (
	"net/http"

	"github.com/gorilla/mux"
	"github.com/jcgr5/apiDomiciliario/handlers"
)

func ServicioIntermediario() {
	router := mux.NewRouter()

	//Definicion de las rutas

	//principal
	router.HandleFunc("/", handlers.Principal)

	//PedirTipo vehiculo
	router.HandleFunc("/tipo", handlers.PedirTipoVehiculo)

	//3 domiciliarios mas cercanos a la ruta indicada
	router.HandleFunc("/domiciliario/{opcion}/{arg1}/{arg2}", handlers.HandDomiciliario)

	//Domiciliarios por tipo de vehiculo
	router.HandleFunc("/tipoVehiculo", handlers.TipoVehiculo)

	//Domiciliarios por tipo de vehiculo
	router.HandleFunc("/ranking", handlers.Ranking)

	//iniciar servidor
	http.ListenAndServe("0.0.0.0:8080", router)
}
