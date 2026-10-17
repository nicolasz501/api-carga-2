
from pydantic import BaseModel, Field
from typing import Optional


class Pregunta(BaseModel):
    id_preguntas: Optional[int] = None
    texto_preguntas: str = Field(min_length=1)
    numero_orden: Optional[int] = Field(default=None, ge=1)
    estado: bool = True
