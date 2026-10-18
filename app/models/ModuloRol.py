
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, AliasChoices


class ModuloRol(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id_modulos_rol: Optional[int] = None

    id_rol: int = Field(
        validation_alias=AliasChoices("id_rol", "role_id")
    )
    id_modulos: int = Field(
        validation_alias=AliasChoices("id_modulos", "module_id")
    )

    puede_ver: bool = False
    puede_crear: bool = False
    puede_editar: bool = False
    puede_eliminar: bool = False
    estado: bool = True
