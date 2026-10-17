
from fastapi import APIRouter, HTTPException

from app.models.ProgramaAcademico import ProgramaAcademico
from app.repositories.programa_academico_repository import (
    ProgramaAcademicoRepository
)


router = APIRouter(
    prefix="/programas-academicos",
    tags=["Gestión de Programas Académicos"]
)

repo = ProgramaAcademicoRepository()


@router.get("/")
def listar_programas():
    try:
        return repo.obtener_todos()

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar los programas académicos"
        )


@router.get("/{programa_id}")
def obtener_programa(programa_id: int):
    try:
        programa = repo.obtener_por_id(programa_id)

        if not programa:
            raise HTTPException(
                status_code=404,
                detail="Programa académico no encontrado"
            )

        return programa

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar el programa académico"
        )


@router.post("/", status_code=201)
def crear_programa(programa: ProgramaAcademico):
    try:
        nuevo_id = repo.crear(programa)

        return {
            "mensaje": "Programa académico registrado exitosamente",
            "id_programas_academicos": nuevo_id
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail=(
                "No se pudo registrar el programa académico. "
                "Verifica que la facultad exista."
            )
        )


@router.put("/{programa_id}")
def actualizar_programa(
    programa_id: int,
    programa: ProgramaAcademico
):
    try:
        actualizado = repo.actualizar(programa_id, programa)

        if not actualizado:
            raise HTTPException(
                status_code=404,
                detail="Programa académico no encontrado"
            )

        return {
            "mensaje": "Programa académico actualizado correctamente",
            "id_programas_academicos": programa_id
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo actualizar el programa académico"
        )


@router.delete("/{programa_id}")
def eliminar_programa(programa_id: int):
    try:
        eliminado = repo.eliminar(programa_id)

        if not eliminado:
            raise HTTPException(
                status_code=404,
                detail="Programa académico no encontrado"
            )

        return {
            "mensaje": "Programa académico eliminado correctamente",
            "id_programas_academicos": programa_id
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail=(
                "No se pudo eliminar el programa. "
                "Verifica si tiene asignaturas asociadas."
            )
        )
