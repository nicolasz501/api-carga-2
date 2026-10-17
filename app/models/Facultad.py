from pydantic import BaseModel
from typing import Optional



class Facultad(BaseModel):
    facultades_id: Optional[int] = None
    nombre_facultades: str
    estado: bool = True
    