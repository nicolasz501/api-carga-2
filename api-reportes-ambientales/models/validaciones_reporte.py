from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ValidacionesReporteBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    reporte_id: int | None = None
    revisor_id: int | None = None
    resultado: str | None = None
    observacion: str | None = None
    fecha_validacion: datetime | None = None

class ValidacionesReporteCrear(ValidacionesReporteBase):
    pass

class ValidacionesReporteActualizar(ValidacionesReporteBase):
    pass
