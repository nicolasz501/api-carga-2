
from fastapi import APIRouter, HTTPException

from app.models.Facultad import Facultad
from app.repositories.facultad_repository import FacultadRepository


router = APIRouter(
    prefix="/facultades",
    tags=["Gestión de Facultades"]
)

repo = FacultadRepository()


@router.get("/")
def listar_facultades():
    try:
        return repo.obtener_todos()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar las facultades"
        )


@router.get("/{facultades_id}")
def obtener_facultad(facultades_id: int):
    try:
        facultad = repo.obtener_por_id(facultades_id)

        if not facultad:
            raise HTTPException(
                status_code=404,
                detail="Facultad no encontrada"
            )

        return facultad

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar la facultad"
        )


@router.post("/", status_code=201)
def crear_facultad(facultad: Facultad):
    try:
        nuevo_id = repo.crear(facultad)

        return {
            "mensaje": "Facultad registrada exitosamente",
            "id_facultades": nuevo_id
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo registrar la facultad"
        )


@router.put("/{facultades_id}")
def actualizar_facultad(
    facultades_id: int,
    facultad: Facultad
):
    try:
        actualizada = repo.actualizar(
            facultades_id,
            facultad
        )

        if not actualizada:
            raise HTTPException(
                status_code=404,
                detail="Facultad no encontrada"
            )

        return {
            "mensaje": "Facultad actualizada correctamente"
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo actualizar la facultad"
        )


@router.delete("/{facultades_id}")
def eliminar_facultad(facultades_id: int):
    try:
        eliminada = repo.eliminar(facultades_id)

        if not eliminada:
            raise HTTPException(
                status_code=404,
                detail="Facultad no encontrada"
            )

        return {
            "mensaje": "Facultad eliminada correctamente"
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo eliminar la facultad. Verifica si tiene programas académicos asociados."
        )
