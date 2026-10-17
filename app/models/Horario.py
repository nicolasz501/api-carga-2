
from pydantic import BaseModel, Field
from typing import Optional
from datetime import time


class Horario(BaseModel):
    id_horarios: Optional[int] = None
    id_carga: int
    dia_laborales: str
    hora_iniciar: time
    hora_finalizar: time
    estado: bool = True

    @classmethod
    def validar_horario(cls, valores):
        return valores
