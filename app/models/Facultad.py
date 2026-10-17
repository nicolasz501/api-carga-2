
from pydantic import BaseModel
from typing import Optional


class Facultad(BaseModel):
    id_facultades: Optional[int] = None
    nombre_facultades: str
    estado: bool = True
