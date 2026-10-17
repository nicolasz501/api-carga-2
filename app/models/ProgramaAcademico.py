
from pydantic import BaseModel, Field
from typing import Optional


class ProgramaAcademico(BaseModel):
    id_programas_academicos: Optional[int] = None
    id_facultades: int
    nombre_programas: str = Field(min_length=1, max_length=100)
    estado: bool = True
