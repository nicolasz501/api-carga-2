
from pydantic import BaseModel
from typing import Optional


class CargaDocente(BaseModel):
    id_carga: Optional[int] = None
    id_usuario: int
    id_periodo: int
    id_grupo: int
    estado: bool = True
