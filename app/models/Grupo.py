
from pydantic import BaseModel
from typing import Optional


class Grupo(BaseModel):
    id_grupo: Optional[int] = None
    id_asignatura: int
    nombre_grupos: str
    estado: bool = True
