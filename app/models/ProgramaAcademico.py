from pydantic import BaseModel
from typing import Optional


class ProgramaAcademico(BaseModel):
    programa_id: Optional[int] = None
    facultades_id: int
    nombre_programa: str
    estado: bool = True

    