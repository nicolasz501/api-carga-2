from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Asignatura(BaseModel):
    asignatura_id: Optional[int] = None
    programa_id: int
    codigo_asignatura: str
    nombres_asignaturas: str
    creditos: int
    estado: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None