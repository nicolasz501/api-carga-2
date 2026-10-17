from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Evaluacion(BaseModel):
    evaluacion_id: Optional[int] = None
    carga_id: int
    periodo_id: int
    tipo_evaluacion: str
    titulo: Optional[str] = None
    fecha_envio: Optional[datetime] = None
    estado: bool = True
    
    