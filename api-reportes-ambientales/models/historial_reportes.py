from datetime import datetime
from pydantic import BaseModel, ConfigDict

class HistorialReportesBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    reporte_id: int | None = None
    usuario_id: int | None = None
    estado_anterior_id: int | None = None
    estado_nuevo_id: int | None = None
    observacion: str | None = None
    fecha_cambio: datetime | None = None

class HistorialReportesCrear(HistorialReportesBase):
    pass

class HistorialReportesActualizar(HistorialReportesBase):
    pass
