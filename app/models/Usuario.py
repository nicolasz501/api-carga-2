# app/models/Usuario.py
from typing import Optional
from pydantic import BaseModel


class UsuarioResponse(BaseModel):
    id_usuario: Optional[int] = None
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    correo: str
    numero_documento: Optional[str] = None
    titulo_academico: Optional[str] = None
    id_rol: int
    estado: bool = True

    class Config:
        from_attributes = True


# Alias para evitar errores si en alguna parte se importa como Usuario
Usuario = UsuarioResponse