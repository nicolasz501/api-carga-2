from datetime import datetime
from pydantic import BaseModel, ConfigDict

class RolesBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nombre_rol: str | None = None
    descripcion: str | None = None
    estado: bool | None = None
    fecha_creacion: datetime | None = None

class RolesCrear(RolesBase):
    pass

class RolesActualizar(RolesBase):
    pass
