from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ModulosPorRolBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    rol_id: int | None = None
    modulo_id: int | None = None
    puede_ver: bool | None = None
    puede_crear: bool | None = None
    puede_editar: bool | None = None
    puede_eliminar: bool | None = None
    estado: bool | None = None

class ModulosPorRolCrear(ModulosPorRolBase):
    pass

class ModulosPorRolActualizar(ModulosPorRolBase):
    pass
