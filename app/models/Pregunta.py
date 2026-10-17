from pydantic import BaseModel
from typing import Optional



class Pregunta(BaseModel):
    pregunta_id: Optional[int] = None
    evaluacion_id: int
    texto_pregunta: str
    numero_orden: int
    estado: bool = True
