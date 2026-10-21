from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ZonasBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nombre_zona: str | None = None
    descripcion: str | None = None
    referencia: str | None = None
    latitud: float | None = None
    longitud: float | None = None
    estado: bool | None = None

class ZonasCrear(ZonasBase):
    pass

class ZonasActualizar(ZonasBase):
    pass
