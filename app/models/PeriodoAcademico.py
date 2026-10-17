
from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import date


class PeriodoAcademico(BaseModel):
    id_periodos_academicos: Optional[int] = None
    codigo_periodo: str = Field(min_length=1, max_length=20)
    fecha_inicio: date
    fecha_finalizar: date
    estado: bool = True

    @model_validator(mode="after")
    def validar_fechas(self):
        if self.fecha_finalizar < self.fecha_inicio:
            raise ValueError(
                "La fecha final no puede ser anterior a la fecha inicial"
            )
        return self
