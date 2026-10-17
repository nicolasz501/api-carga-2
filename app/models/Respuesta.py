
from pydantic import BaseModel, Field
from typing import Optional


class Respuesta(BaseModel):
    id_respuestas: Optional[int] = None
    id_pregunta_evaluacion: int = Field(gt=0)
    id_usuario: int = Field(gt=0)
    puntaje: int = Field(ge=1, le=5)
    comentario: Optional[str] = Field(default=None, max_length=2000)
    estado: bool = True
