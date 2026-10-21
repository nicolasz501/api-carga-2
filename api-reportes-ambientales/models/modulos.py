from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ModulosBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nombre_modulo: str | None = None
    descripcion: str | None = None
    ruta: str | None = None
    icono: str | None = None
    estado: bool | None = None
    fecha_creacion: datetime | None = None

class ModulosCrear(ModulosBase):
    pass

class ModulosActualizar(ModulosBase):
    pass
