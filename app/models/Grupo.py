from pydantic import BaseModel
from typing import Optional



class Grupo(BaseModel):
    grupos_id: Optional[int] = None
    asignaturas_id: int
    periodos_id: int
    nombre_grupos: str
    capacidad: int
    estado: bool = True
    