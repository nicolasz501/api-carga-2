from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Usuario(BaseModel):
    usuario_id: Optional[int] = None
    facultades_id: Optional[int] = None
    rol_id: int
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    correo: str
    contraseña: str
    numero_documento: str
    codigo_personal: Optional[str] = None
    titulo_academico: Optional[str] = None
    estado: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
