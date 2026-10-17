
from fastapi import APIRouter, HTTPException

from app.models.PeriodoAcademico import PeriodoAcademico
from app.repositories.periodo_academico_repository import (
    PeriodoAcademicoRepository
)


router = APIRouter(
    prefix="/periodos-academicos",
    tags=["Gestión de Períodos Académicos"]
)

repo = PeriodoAcademicoRepository()


@router.get("/")
def listar_periodos():
    try:
        return repo.obtener_todos()

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar los períodos académicos"
        )


@router.get("/{periodo_id}")
def obtener_periodo(periodo_id: int):
    try:
        periodo = repo.obtener_por_id(periodo_id)

        if not periodo:
            raise HTTPException(
                status_code=404,
                detail="Período académico no encontrado"
            )

        return periodo

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar el período académico"
        )


@router.post("/", status_code=201)
def crear_periodo(periodo: PeriodoAcademico):
    try:
        nuevo_id = repo.crear(periodo)

        return {
            "mensaje": "Período académico registrado exitosamente",
            "id_periodos_academicos": nuevo_id
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo registrar el período académico"
        )


@router.put("/{periodo_id}")
def actualizar_periodo(
    periodo_id: int,
    periodo: PeriodoAcademico
):
    try:
        actualizado = repo.actualizar(periodo_id, periodo)

        if not actualizado:
            raise HTTPException(
                status_code=404,
                detail="Período académico no encontrado"
            )

        return {
            "mensaje": "Período académico actualizado correctamente",
            "id_periodos_academicos": periodo_id
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo actualizar el período académico"
        )


@router.delete("/{periodo_id}")
def eliminar_periodo(periodo_id: int):
    try:
        eliminado = repo.eliminar(periodo_id)

        if not eliminado:
            raise HTTPException(
                status_code=404,
                detail="Período académico no encontrado"
            )

        return {
            "mensaje": "Período académico eliminado correctamente",
            "id_periodos_academicos": periodo_id
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail=(
                "No se pudo eliminar el período. "
                "Verifica si tiene cargas docentes asociadas."
            )
        )
