from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ModuloRol(BaseModel):
    modules_rol_id: Optional[int] = None
    role_id: int
    module_id: int
    puede_ver: bool
    puede_crear: bool = False
    puede_editar: bool = False
    puede_eliminar: bool = False
    estado: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    