
from fastapi import APIRouter, HTTPException

from app.models.Modulo import Modulo
from app.repositories.modulo_repository import ModuloRepository


router = APIRouter(
    prefix="/modulos",
    tags=["Gestión de Módulos"]
)

repo = ModuloRepository()


@router.get("/")
def listar_modulos():
    return repo.obtener_todos()


@router.get("/{modulos_id}")
def obtener_modulo(modulos_id: int):
    modulo = repo.obtener_por_id(modulos_id)

    if not modulo:
        raise HTTPException(
            status_code=404,
            detail="Módulo no encontrado"
        )

    return modulo


@router.post("/")
def crear_modulo(modulo: Modulo):
    try:
        nuevo_id = repo.crear(modulo)
    except Exception as e:
        print(f"Error al crear módulo: {e}")
        raise HTTPException(
            status_code=500,
            detail="No se pudo registrar el módulo"
        )

    return {
        "mensaje": "Módulo registrado exitosamente",
        "id_modulos": nuevo_id
    }


@router.put("/{modulos_id}")
def actualizar_modulo(modulos_id: int, modulo: Modulo):
    actualizado = repo.actualizar(modulos_id, modulo)

    if not actualizado:
        raise HTTPException(
            status_code=404,
            detail="Módulo no encontrado o no actualizado"
        )

    return {"mensaje": "Módulo actualizado correctamente"}


@router.delete("/{modulos_id}")
def eliminar_modulo(modulos_id: int):
    try:
        eliminado = repo.eliminar(modulos_id)
    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Módulo no encontrado"
        )

    return {"mensaje": "Módulo eliminado correctamente"}
