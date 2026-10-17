from pydantic import BaseModel
from typing import Optional


class CargaDocente(BaseModel):
    carga_id: Optional[int] = None
    user_id: int
    periodo_id: int
    id_grupo: int
    estado: bool = True
    
    