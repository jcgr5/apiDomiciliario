package handlers

import (
	//"fmt"
	"encoding/json"
	"fmt"
	"io"
	"net/http"

	"github.com/gorilla/mux"
)

type DomiciliarioRanking struct {
	ID                    int    `json:"Id"`
	Nombre                string `json:"Nombre"`
	TipoVehiculo          string `json:"TipoVehiculo"`
	EstrellasCalificacion int    `json:"EstrellasCalificacion"`
}

type RespuestaRanking struct {
	RankingDom []DomiciliarioRanking `json:"Ranking"`
}

func generarListaRanking(ranking []DomiciliarioRanking) string {
	var lista string
	for _, item := range ranking {
		lista += fmt.Sprintf(`<li>ID: %d, Nombre: %s,TipoVehiculo: %s,EstrellasCalificacion: %d</li>`,
			item.ID, item.Nombre, item.TipoVehiculo, item.EstrellasCalificacion)
	}
	return lista
}

type DomiciliarioTipoVehiculo struct {
	ID                    int     `json:"ID"`
	Nombre                string  `json:"Nombre"`
	UbicacionDomiciliario string  `json:"UbicacionDomiciliario"`
	Tarifa                float64 `json:"Tarifa"`
	TipoVehiculo          string  `json:"TipoVehiculo"`
	EstrellasCalificacion int     `json:"EstrellasCalificacion"`
}

type RespuestaTipoVehiculo struct {
	Tipo []DomiciliarioTipoVehiculo
}

func generarListaTipoVehiculo(Tipo []DomiciliarioTipoVehiculo) string {
	var lista string
	for _, item := range Tipo {
		lista += fmt.Sprintf(`<li>ID: %d, Nombre: %s,UbicacionDomiciliario: %s, Tarifa: %f,TipoVehiculo: %s,EstrellasCalificacion: %d</li>`,
			item.ID, item.Nombre, item.UbicacionDomiciliario, item.Tarifa, item.TipoVehiculo, item.EstrellasCalificacion)
	}
	return lista
}

type DomiciliarioPy struct {
	ID        int     `json:"id"`
	Nombre    string  `json:"Nombre"`
	X         float64 `json:"X"`
	Y         float64 `json:"Y"`
	Distancia float64 `json:"distancia"`
}

type Respuesta struct {
	FileName    string           `json:"nombreArchivo"`
	ImageBase64 string           `json:"contenidoArchivo"`
	MasCercanos []DomiciliarioPy `json:"masCercanos"`
}

type QueryRequest struct {
	SQLQuery string `json:"opcion"`
}

// QueryResponse es la estructura que representa la respuesta JSON que contiene el resultado.
type QueryResponse struct {
	Result string `json:"result"`
}

func generarLista(masCercanos []DomiciliarioPy) string {
	var lista string
	for _, item := range masCercanos {
		lista += fmt.Sprintf(`<li>ID: %d, Nombre: %s,Distancia al Cliente: %f</li>`,
			item.ID, item.Nombre, item.Distancia)
	}
	return lista
}

func Principal(w http.ResponseWriter, r *http.Request) {
	http.ServeFile(w, r, "index.html")
}

func PedirTipoVehiculo(w http.ResponseWriter, r *http.Request) {
	http.ServeFile(w, r, "TipoVehiculo.html")
}

func HandDomiciliario(w http.ResponseWriter, r *http.Request) {

	op := mux.Vars(r)
	//Instanciar cliente para consumir el servicio
	cliente := http.Client{}

	//Solicitud get a la api de Python
	//resp, err := cliente.Get("http://localhost:5000/otro-endpoint?nombreAdjunto=Juancho&numero=69")

	url := fmt.Sprintf("http://127.0.0.1:8000/domiciliarioMasCercano?coorCliente1=%s&coorCliente2=%s", op["arg1"], op["arg2"])

	// An error is returned if something goes wrong
	resp, err := cliente.Get(url)
	if err != nil {
		http.Error(w, "Error al realizar la solicitud al servicio externo", http.StatusInternalServerError)
	}

	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		http.Error(w, "Error en la respuesta del servicio externo", http.StatusInternalServerError)
		return
	}

	cuerpo, err := io.ReadAll(resp.Body)
	if err != nil {
		http.Error(w, "Error al leer el cuerpo de la respuesta", http.StatusInternalServerError)
		return
	}

	var respuesta Respuesta
	err = json.Unmarshal(cuerpo, &respuesta)
	if err != nil {
		http.Error(w, "Error al decodificar la respuesta del script", http.StatusInternalServerError)
		return
	}

	//Retornar la respuesta obtenida por el canal de respuestas a requests http
	//cambiar el header de la respuesta para que envie json
	w.Header().Set("Content-Type", "text/html")
	w.WriteHeader(http.StatusOK)
	htmlResponse := fmt.Sprintf(`
	<html>
	<body>
		<h1>Asignacion de los domiciliarios mas cercanos</h1>
		<h2>Domiciliarios Mas Cercanos:</h2>
		<ul>
                %s
        </ul>
		<img src="data:image/png;base64,%s" alt="%s">
	</body>
	</html>`, generarLista(respuesta.MasCercanos), respuesta.ImageBase64, respuesta.FileName)
	w.Write([]byte(htmlResponse))
}

func TipoVehiculo(w http.ResponseWriter, r *http.Request) {
	// Obtener el tipo de vehículo de los parámetros de consulta
	tipoVehiculo := r.URL.Query().Get("tipo")
	if tipoVehiculo == "" {
		http.Error(w, "El parámetro 'tipo' es requerido", http.StatusBadRequest)
		return
	}

	cliente := http.Client{}

	//cambiar ruta
	url := fmt.Sprintf("http://127.0.0.1:8081/TipoVehiculo?tipo=%s", tipoVehiculo)

	// An error is returned if something goes wrong
	resp, err := cliente.Get(url)
	if err != nil {
		http.Error(w, "Error al realizar la solicitud al servicio externo", http.StatusInternalServerError)
	}

	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		http.Error(w, "Error en la respuesta del servicio externo", http.StatusInternalServerError)
		return
	}

	cuerpo, err := io.ReadAll(resp.Body)
	if err != nil {
		http.Error(w, "Error al leer el cuerpo de la respuesta", http.StatusInternalServerError)
		return
	}

	var respuesta RespuestaTipoVehiculo
	err = json.Unmarshal(cuerpo, &respuesta.Tipo)
	if err != nil {
		http.Error(w, "Error al decodificar la respuesta del script", http.StatusInternalServerError)
		return
	}

	//Retornar la respuesta obtenida por el canal de respuestas a requests http
	//cambiar el header de la respuesta para que envie json
	w.Header().Set("Content-Type", "text/html")
	w.WriteHeader(http.StatusOK)
	htmlResponse := fmt.Sprintf(`
	<html>
	<body>
		<h1>Domiciliarios por tipo de vehiculo seleccionado</h1>
		<h2>Domiciliarios:</h2>
		<ul>
                %s
        </ul>
	</body>
	</html>`, generarListaTipoVehiculo(respuesta.Tipo))
	w.Write([]byte(htmlResponse))
}

func Ranking(w http.ResponseWriter, r *http.Request) {

	//Instanciar cliente para consumir el servicio
	cliente := http.Client{}

	url := "http://127.0.0.1:8001/Rankig"

	// An error is returned if something goes wrong
	resp, err := cliente.Get(url)
	if err != nil {
		http.Error(w, "Error al realizar la solicitud al servicio externo", http.StatusInternalServerError)
	}

	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		http.Error(w, "Error en la respuesta del servicio externo", http.StatusInternalServerError)
		return
	}

	cuerpo, err := io.ReadAll(resp.Body)
	if err != nil {
		http.Error(w, "Error al leer el cuerpo de la respuesta", http.StatusInternalServerError)
		return
	}

	var respuesta RespuestaRanking
	err = json.Unmarshal(cuerpo, &respuesta)
	if err != nil {
		http.Error(w, "Error al decodificar la respuesta del script", http.StatusInternalServerError)
		return
	}

	//Retornar la respuesta obtenida por el canal de respuestas a requests http
	//cambiar el header de la respuesta para que envie json
	w.Header().Set("Content-Type", "text/html")
	w.WriteHeader(http.StatusOK)
	htmlResponse := fmt.Sprintf(`
	<html>
	<body>
		<h1>Rankig domiciliarios con mejor calificacion</h1>
		<h2>Domiciliarios:</h2>
		<ul>
                %s
        </ul>
	</body>
	</html>`, generarListaRanking(respuesta.RankingDom))
	w.Write([]byte(htmlResponse))
}
