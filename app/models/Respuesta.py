
from pydantic import BaseModel, Field
from typing import Optional

class Respuesta(BaseModel):
    respuesta_id: Optional[int] = None
    pregunta_id: int
    usuario_id: Optional[int] = None
    puntaje: int = Field(ge=1, le=5)
    comentario: Optional[str] = Field(default=None, max_length=500)
    estado: bool = True

