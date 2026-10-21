from datetime import datetime
from pydantic import BaseModel, ConfigDict

class UsuariosBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    rol_id: int | None = None
    nombres: str | None = None
    apellidos: str | None = None
    correo: str | None = None
    contrasena_hash: str | None = None
    telefono: str | None = None
    documento: str | None = None
    estado: bool | None = None
    fecha_creacion: datetime | None = None
    fecha_actualizacion: datetime | None = None

class UsuariosCrear(UsuariosBase):
    pass

class UsuariosActualizar(UsuariosBase):
    pass
