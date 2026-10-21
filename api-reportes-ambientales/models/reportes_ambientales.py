from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator


class ReportesAmbientalesCrear(BaseModel):
    model_config = ConfigDict(extra="forbid")

    categoria_id: int
    zona_id: int
    titulo: str = Field(min_length=5, max_length=200)
    descripcion: str = Field(min_length=10, max_length=5000)

    direccion_referencia: str | None = Field(
        default=None,
        max_length=300,
    )
    latitud: float | None = Field(default=None, ge=-90, le=90)
    longitud: float | None = Field(default=None, ge=-180, le=180)
    fecha_incidente: datetime | None = None

    @field_validator("titulo", "descripcion")
    @classmethod
    def validar_texto(cls, valor: str) -> str:
        valor = valor.strip()

        if not valor:
            raise ValueError("Este campo no puede estar vacío")

        return valor


class ReportesAmbientalesActualizar(BaseModel):
    model_config = ConfigDict(extra="forbid")

    categoria_id: int | None = None
    zona_id: int | None = None
    titulo: str | None = Field(default=None, min_length=5, max_length=200)
    descripcion: str | None = Field(
        default=None,
        min_length=10,
        max_length=5000,
    )
    direccion_referencia: str | None = Field(default=None, max_length=300)
    latitud: float | None = Field(default=None, ge=-90, le=90)
    longitud: float | None = Field(default=None, ge=-180, le=180)
    fecha_incidente: datetime | None = None

    @field_validator("titulo", "descripcion")
    @classmethod
    def validar_texto(cls, valor: str | None) -> str | None:
        if valor is None:
            return valor

        valor = valor.strip()

        if not valor:
            raise ValueError("Este campo no puede estar vacío")

        return valor