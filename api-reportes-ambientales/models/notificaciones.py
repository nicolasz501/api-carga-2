from datetime import datetime
from pydantic import BaseModel, ConfigDict

class NotificacionesBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    usuario_id: int | None = None
    reporte_id: int | None = None
    titulo: str | None = None
    mensaje: str | None = None
    leida: bool | None = None
    fecha_creacion: datetime | None = None
    fecha_lectura: datetime | None = None

class NotificacionesCrear(NotificacionesBase):
    pass

class NotificacionesActualizar(NotificacionesBase):
    pass
