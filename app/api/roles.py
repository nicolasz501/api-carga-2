
from fastapi import APIRouter, HTTPException

from app.models.Rol import Rol
from app.repositories.rol_repository import RolRepository


router = APIRouter(
    prefix="/roles",
    tags=["Gestión de Roles"]
)

repo = RolRepository()


@router.get("/")
def listar_roles():
    return repo.obtener_todos()


@router.get("/{rol_id}")
def obtener_rol(rol_id: int):
    rol = repo.obtener_por_id(rol_id)

    if not rol:
        raise HTTPException(
            status_code=404,
            detail="Rol no encontrado"
        )

    return rol


@router.post("/")
def crear_rol(rol: Rol):
    try:
        nuevo_id = repo.crear(rol)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    return {
        "mensaje": "Rol registrado exitosamente",
        "id_roles": nuevo_id
    }


@router.put("/{rol_id}")
def actualizar_rol(rol_id: int, rol: Rol):
    try:
        actualizado = repo.actualizar(rol_id, rol)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    if not actualizado:
        raise HTTPException(
            status_code=404,
            detail="Rol no encontrado"
        )

    return {"mensaje": "Rol actualizado correctamente"}


@router.delete("/{rol_id}")
def eliminar_rol(rol_id: int):
    try:
        eliminado = repo.eliminar(rol_id)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Rol no encontrado"
        )

    return {"mensaje": "Rol eliminado correctamente"}
