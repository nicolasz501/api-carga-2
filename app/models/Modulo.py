
from typing import Optional
from pydantic import BaseModel, ConfigDict


class Modulo(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id_modulos: Optional[int] = None
    nombre_modulos: str
    estado: bool = True
