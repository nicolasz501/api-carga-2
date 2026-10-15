from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Modulo(BaseModel):
    modulos_id: Optional[int] = None
    nombre_modulo: str
    estado: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None