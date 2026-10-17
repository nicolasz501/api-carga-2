
from pydantic import BaseModel, Field
from typing import Optional


class Asignatura(BaseModel):
    id_asignatura: Optional[int] = None
    id_programa: int
    codigo_asignatura: str
    nombre_asignatura: str
    creditos: int = Field(gt=0)
    estado: bool = True
