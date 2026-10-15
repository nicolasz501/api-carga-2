from fastapi import APIRouter, HTTPException

from app.models.ModuloRol import ModuloRol
from app.repositories.modulo_rol_repository import ModuloRolRepository


router = APIRouter(prefix="/modulos-rol",tags=["Gestión de Módulos por Rol"])
repo = ModuloRolRepository()


@router.get("/")
def listar_modulos_rol():
    return repo.obtener_todos()


@router.get("/{modules_rol_id}")
def obtener_modulo_rol(modules_rol_id: int):
    modulo_rol = repo.obtener_por_id(modules_rol_id)

    if not modulo_rol:
        raise HTTPException(status_code=404,detail="Módulo-Rol no encontrado")

    return modulo_rol


@router.post("/")
def crear_modulo_rol(modulo_rol: ModuloRol):
    nuevo_id = repo.crear(modulo_rol)

    return {"mensaje": "Módulo-Rol registrado exitosamente","id": nuevo_id}


@router.delete("/{modules_rol_id}")
def eliminar_modulo_rol(modules_rol_id: int):
    exito = repo.eliminar(modules_rol_id)

    if not exito:
        raise HTTPException(status_code=404,detail="Módulo-Rol no encontrado")

    return { "mensaje": "Módulo-Rol eliminado correctamente"}


@router.put("/{modules_rol_id}")
def actualizar_modulo_rol(modules_rol_id: int,modulo_rol: ModuloRol):
    exito = repo.actualizar(modules_rol_id, modulo_rol)

    if not exito:
        raise HTTPException(status_code=404,detail="Módulo-Rol no encontrado")

    return {"mensaje": "Módulo-Rol actualizado correctamente"}