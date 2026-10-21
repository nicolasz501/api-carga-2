from datetime import datetime
from pydantic import BaseModel, ConfigDict

class EstadosReporteBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nombre_estado: str | None = None
    descripcion: str | None = None
    estado: bool | None = None

class EstadosReporteCrear(EstadosReporteBase):
    pass

class EstadosReporteActualizar(EstadosReporteBase):
    pass
