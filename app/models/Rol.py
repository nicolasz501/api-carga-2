
from typing import Optional
from pydantic import BaseModel, ConfigDict


class Rol(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id_roles: Optional[int] = None
    nombre_rol: str
    estado: bool = True
