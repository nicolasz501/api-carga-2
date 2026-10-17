from pydantic import BaseModel
from typing import Optional
from datetime import date


class PeriodoAcademico(BaseModel):

    periodo_id: Optional[int] = None
    codigo_periodo: str
    fecha_inicio: date
    fecha_finalizar: date
    estado: bool = True
   