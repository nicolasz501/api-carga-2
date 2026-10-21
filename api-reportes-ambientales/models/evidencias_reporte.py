from datetime import datetime
from pydantic import BaseModel, ConfigDict

class EvidenciasReporteBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    reporte_id: int | None = None
    url_archivo: str | None = None
    nombre_archivo: str | None = None
    tipo_archivo: str | None = None
    fecha_subida: datetime | None = None

class EvidenciasReporteCrear(EvidenciasReporteBase):
    pass

class EvidenciasReporteActualizar(EvidenciasReporteBase):
    pass
