from fastapi import APIRouter, HTTPException

from app.models.Rol import Rol
from app.repositories.rol_repository import RolRepository


router = APIRouter(prefix="/roles",tags=["Gestión de Roles"])
repo = RolRepository()


@router.get("/")
def listar_roles():
    return repo.obtener_todos()


@router.get("/{rol_id}")
def obtener_rol(rol_id: int):
    rol = repo.obtener_por_id(rol_id)

    if not rol:
        raise HTTPException(status_code=404,detail="Rol no encontrado")

    return rol


@router.post("/")
def crear_rol(rol: Rol):
    nuevo_id = repo.crear(rol)

    return {"mensaje": "Rol registrado exitosamente","id": nuevo_id}


@router.delete("/{rol_id}")
def eliminar_rol(rol_id: int):
    exito = repo.eliminar(rol_id)

    if not exito:
        raise HTTPException(status_code=404,detail="Rol no encontrado")

    return {"mensaje": "Rol eliminado correctamente"}


@router.put("/{rol_id}")
def actualizar_rol(rol_id: int, rol: Rol):
    exito = repo.actualizar(rol_id, rol)

    if not exito:
        raise HTTPException( status_code=404, detail="Rol no encontrado")

    return {"mensaje": "Rol actualizado correctamente"}