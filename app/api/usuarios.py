from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Importación segura compatible con cualquier estructura de modelos
try:
    from app.models.Usuario import UsuarioResponse as Usuario
except ImportError:
    try:
        from app.models.Usuario import Usuario
    except ImportError:
        from app.models.usuario import Usuario

from app.repositories.usuario_repository import UsuarioRepository

router = APIRouter(
    prefix="/usuarios",
    tags=["Gestión de Usuarios"]
)

repo = UsuarioRepository()


class LoginRequest(BaseModel):
    correo: str
    password: str


class UsuarioUpdate(BaseModel):
    id_rol: int
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    correo: str
    numero_documento: str
    titulo_academico: Optional[str] = None  # Agregado para soportar título académico
    estado: bool = True
    contrasena: Optional[str] = None


@router.get("/")
def listar_usuarios():
    return repo.obtener_todos()


@router.post("/login")
def login(datos: LoginRequest):
    resultado = repo.login(datos.correo, datos.password)

    if not resultado:
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos"
        )

    return resultado


@router.get("/{usuario_id}")
def obtener_usuario(usuario_id: int):
    usuario = repo.obtener_por_id(usuario_id)

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return usuario


@router.post("/")
def crear_usuario(usuario: Usuario):
    try:
        nuevo_id = repo.crear(usuario)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    if nuevo_id is None:
        raise HTTPException(
            status_code=500,
            detail="No se pudo crear el usuario"
        )

    return {
        "mensaje": "Usuario registrado exitosamente",
        "id_usuario": nuevo_id
    }


@router.put("/{usuario_id}")
def actualizar_usuario(usuario_id: int, usuario: UsuarioUpdate):
    try:
        actualizado = repo.actualizar(usuario_id, usuario)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    if not actualizado:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return {"mensaje": "Usuario actualizado correctamente"}


@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int):
    try:
        eliminado = repo.eliminar(usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return {"mensaje": "Usuario eliminado correctamente"}