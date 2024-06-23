package handlers

import (
	"encoding/json"
	"net/http"
	"os/exec"
)

type QueryRequest struct {
	SQLQuery string `json:"opcion"`
}

// QueryResponse es la estructura que representa la respuesta JSON que contiene el resultado.
type QueryResponse struct {
	Result interface{} `json:"result"`
}

func MasCercano(w http.ResponseWriter, r *http.Request) {
	var req QueryRequest

	// Decodificar la solicitud JSON
	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// Ejecutar el script Python con la consulta SQL
	cmd := exec.Command("python3", "db.py", req.SQLQuery)
	output, err := cmd.Output()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Decodificar la salida JSON del script Python
	var result QueryResponse
	if err := json.Unmarshal(output, &result); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Codificar la respuesta en JSON
	w.Header().Set("Content-Type", "application/json")
	if err := json.NewEncoder(w).Encode(result); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
}
