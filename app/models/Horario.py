from pydantic import BaseModel
from typing import Optional
from datetime import  time


class Horario(BaseModel):
    horario_id: Optional[int] = None
    carga_id: int
    dia_laborales: int
    hora_inicio: time
    hora_finalizar: time
    estado: bool = True
   