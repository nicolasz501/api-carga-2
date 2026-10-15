from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Rol(BaseModel):
    rol_id: Optional[int] = None
    nombre_rol: str
    estado: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None