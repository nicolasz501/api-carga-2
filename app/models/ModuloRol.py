
from pydantic import BaseModel, Field
from typing import Optional


class ModuloRol(BaseModel):
    id_modulos_rol: Optional[int] = None
    id_rol: int
    id_modulos: int

    puede_ver: bool = False
    puede_crear: bool = False
    puede_editar: bool = False
    puede_eliminar: bool = False
    estado: bool = True
