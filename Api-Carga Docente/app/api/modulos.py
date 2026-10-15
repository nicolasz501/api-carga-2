from fastapi import APIRouter, HTTPException

from app.models.Modulo import Modulo
from app.repositories.modulo_repository import ModuloRepository


router = APIRouter(prefix="/modulos",tags=["Gestión de Módulos"])
repo = ModuloRepository()


@router.get("/")
def listar_modulos():
    return repo.obtener_todos()


@router.get("/{modulos_id}")
def obtener_modulo(modulos_id: int):
    modulo = repo.obtener_por_id(modulos_id)

    if not modulo:
        raise HTTPException(status_code=404,detail="Módulo no encontrado")

    return modulo


@router.post("/")
def crear_modulo(modulo: Modulo):
    nuevo_id = repo.crear(modulo)

    return {"mensaje": "Módulo registrado exitosamente","id": nuevo_id}


@router.delete("/{modulos_id}")
def eliminar_modulo(modulos_id: int):
    exito = repo.eliminar(modulos_id)

    if not exito:
        raise HTTPException(status_code=404,detail="Módulo no encontrado")

    return {"mensaje": "Módulo eliminado correctamente"}


@router.put("/{modulos_id}")
def actualizar_modulo(modulos_id: int,modulo: Modulo):
    exito = repo.actualizar(modulos_id, modulo)

    if not exito:
        raise HTTPException(status_code=404,detail="Módulo no encontrado")

    return { "mensaje": "Módulo actualizado correctamente"}