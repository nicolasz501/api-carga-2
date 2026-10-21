from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CategoriasIncidenteBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nombre_categoria: str | None = None
    descripcion: str | None = None
    estado: bool | None = None
    fecha_creacion: datetime | None = None

class CategoriasIncidenteCrear(CategoriasIncidenteBase):
    pass

class CategoriasIncidenteActualizar(CategoriasIncidenteBase):
    pass
