from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class PeriodoAcademico(BaseModel):
    periodo_id: Optional[int] = None
    codigo_periodo: str
    fecha_inicio: date
    fecha_finalizar: date
    estado: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None