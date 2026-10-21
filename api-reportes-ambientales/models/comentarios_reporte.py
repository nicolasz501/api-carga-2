from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ComentariosReporteBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    reporte_id: int | None = None
    usuario_id: int | None = None
    comentario: str | None = None
    fecha_comentario: datetime | None = None
    estado: bool | None = None

class ComentariosReporteCrear(ComentariosReporteBase):
    pass

class ComentariosReporteActualizar(ComentariosReporteBase):
    pass
