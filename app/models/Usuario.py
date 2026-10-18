# app/models/Usuario.py
from pydantic import BaseModel
from typing import Optional

class Usuario(BaseModel):
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