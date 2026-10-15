from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time


class Horario(BaseModel):
    horario_id: Optional[int] = None
    carga_id: int
    dia_laborales: int
    hora_inicio: time
    hora_finalizar: time
    estado: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None