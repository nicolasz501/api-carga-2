
from typing import Optional
from pydantic import BaseModel, ConfigDict


class Usuario(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id_usuario: Optional[int] = None
    id_rol: int

    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None

    correo: str
    contrasena: str
    numero_documento: str
    estado: bool = True
