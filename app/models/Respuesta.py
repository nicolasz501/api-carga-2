from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Respuesta(BaseModel):
    respuesta_id: Optional[int] = None
    pregunta_id: int
    puntaje: int
    comentario: Optional[str] = None
    estado: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None