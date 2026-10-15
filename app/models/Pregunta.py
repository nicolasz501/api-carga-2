from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Pregunta(BaseModel):
    pregunta_id: Optional[int] = None
    evaluacion_id: int
    texto_pregunta: str
    numero_orden: int
    estado: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None