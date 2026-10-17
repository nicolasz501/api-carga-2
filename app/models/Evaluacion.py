
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Evaluacion(BaseModel):
    id_evaluaciones: Optional[int] = None
    id_carga: int
    tipo_evaluacion: str
    titulo: str
    fecha_envio: Optional[datetime] = None
    estado: bool = True
