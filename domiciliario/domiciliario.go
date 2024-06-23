package domiciliario

type Domiciliario struct {
	Id_Domiciliario       int     `json:"Id_Domiciliario"`
	Nombre                string  `json:"Nombre"`
	UbicacionDomiciliario string  `json:"UbicacionDomiciliario"`
	tarifa                float64 `json:"tarifa"`
	FotoDomiciliario      int     `json:"FotoDomiciliario"`
	TipoVehiculo          string  `json:"TipoVehiculo"`
	EstrellasCalificacion int     `json:"EstrellasCalificacion"`
}
