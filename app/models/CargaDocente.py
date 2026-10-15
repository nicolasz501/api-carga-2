from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CargaDocente(BaseModel):
    carga_id: Optional[int] = None
    user_id: int
    periodo_id: int
    id_grupo: int
    estado: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    