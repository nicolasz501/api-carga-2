
from fastapi import APIRouter, HTTPException

from app.models.Asignatura import Asignatura
from app.repositories.asignatura_repository import AsignaturaRepository


router = APIRouter(
    prefix="/asignaturas",
    tags=["Gestión de Asignaturas"]
)

repo = AsignaturaRepository()


@router.get("/")
def listar_asignaturas():
    try:
        return repo.obtener_todos()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar las asignaturas"
        )


@router.get("/{asignatura_id}")
def obtener_asignatura(asignatura_id: int):
    try:
        asignatura = repo.obtener_por_id(asignatura_id)

        if not asignatura:
            raise HTTPException(
                status_code=404,
                detail="Asignatura no encontrada"
            )

        return asignatura

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar la asignatura"
        )


@router.post("/", status_code=201)
def crear_asignatura(asignatura: Asignatura):
    try:
        nuevo_id = repo.crear(asignatura)

        return {
            "mensaje": "Asignatura registrada exitosamente",
            "id_asignatura": nuevo_id
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo registrar la asignatura. Verifica que el programa académico exista y que el código sea válido."
        )


@router.put("/{asignatura_id}")
def actualizar_asignatura(
    asignatura_id: int,
    asignatura: Asignatura
):
    try:
        actualizada = repo.actualizar(
            asignatura_id,
            asignatura
        )

        if not actualizada:
            raise HTTPException(
                status_code=404,
                detail="Asignatura no encontrada"
            )

        return {
            "mensaje": "Asignatura actualizada correctamente"
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo actualizar la asignatura"
        )


@router.delete("/{asignatura_id}")
def eliminar_asignatura(asignatura_id: int):
    try:
        eliminada = repo.eliminar(asignatura_id)

        if not eliminada:
            raise HTTPException(
                status_code=404,
                detail="Asignatura no encontrada"
            )

        return {
            "mensaje": "Asignatura eliminada correctamente"
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo eliminar la asignatura. Comprueba si existen grupos asociados."
        )
