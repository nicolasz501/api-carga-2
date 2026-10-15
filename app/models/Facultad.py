from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Facultad(BaseModel):
    facultades_id: Optional[int] = None
    nombre_facultades: str
    estado: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None