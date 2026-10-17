
from typing import Optional

from pydantic import BaseModel, Field


class PreguntaEvaluacion(BaseModel):
    id_pregunta_evaluacion: Optional[int] = None
    id_preguntas: int = Field(gt=0)
    id_evaluacion: int = Field(gt=0)
    numero_orden: int = Field(ge=1)
    estado: bool = True
