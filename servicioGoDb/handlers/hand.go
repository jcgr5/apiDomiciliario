package handlers

import (
	//"fmt"
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/jcgr5/apiDomiciliario/DBgo"
)

func TipoVehiculo(w http.ResponseWriter, r *http.Request) {

	// Obtener el tipo de vehículo de los parámetros de consulta
	tipoVehiculo := r.URL.Query().Get("tipo")
	if tipoVehiculo == "" {
		http.Error(w, "El parámetro 'tipo' es requerido", http.StatusBadRequest)
		return
	}

	resp, err := DBgo.Conexion(tipoVehiculo)
	if err != nil {
		http.Error(w, "Error al obtener domiciliarios: ", http.StatusInternalServerError)
	}

	// Configurar el encabezado de respuesta para JSON
	w.Header().Set("Content-Type", "application/json")

	// Codificar y devolver los domiciliarios como JSON
	if err := json.NewEncoder(w).Encode(resp); err != nil {
		http.Error(w, fmt.Sprintf("Error al codificar la respuesta: %v", err), http.StatusInternalServerError)
		return
	}
}
