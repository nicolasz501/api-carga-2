from fastapi import APIRouter, HTTPException

from app.models.PeriodoAcademico import PeriodoAcademico
from app.repositories.periodo_academico_repository import PeriodoAcademicoRepository


router = APIRouter(
    prefix="/periodos-academicos",
    tags=["Gestión de Períodos Académicos"]
)

repo = PeriodoAcademicoRepository()


@router.get("/")
def listar_periodos():
    try:
        return repo.obtener_todos()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener los períodos académicos: {str(e)}"
        )


@router.get("/{periodo_id}")
def obtener_periodo(periodo_id: int):

    periodo = repo.obtener_por_id(periodo_id)

    if not periodo:
        raise HTTPException(
            status_code=404,
            detail="Período académico no encontrado"
        )

    return periodo


@router.post("/")
def crear_periodo(periodo: PeriodoAcademico):

    nuevo_id = repo.crear(periodo)

    if not nuevo_id:
        raise HTTPException(
            status_code=500,
            detail="No se pudo crear el período académico"
        )

    return {
        "mensaje": "Período académico registrado exitosamente",
        "periodo_id": nuevo_id
    }


@router.put("/{periodo_id}")
def actualizar_periodo(
    periodo_id: int,
    periodo: PeriodoAcademico
):

    actualizado = repo.actualizar(
        periodo_id,
        periodo
    )

    if not actualizado:
        raise HTTPException(
            status_code=404,
            detail="Período académico no encontrado"
        )

    return {
        "mensaje": "Período académico actualizado correctamente",
        "periodo_id": periodo_id
    }


@router.delete("/{periodo_id}")
def eliminar_periodo(periodo_id: int):

    eliminado = repo.eliminar(periodo_id)

    if not eliminado:
        raise HTTPException(
            status_code=404,
            detail="Período académico no encontrado"
        )

    return {
        "mensaje": "Período académico eliminado correctamente",
        "periodo_id": periodo_id
    }