from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProgramaAcademico(BaseModel):
    programa_id: Optional[int] = None
    facultades_id: int
    nombre_programa: str
    estado: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    