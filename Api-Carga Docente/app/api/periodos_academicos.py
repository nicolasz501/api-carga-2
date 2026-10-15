from fastapi import APIRouter, HTTPException

from app.models.PeriodoAcademico import PeriodoAcademico
from app.repositories.periodo_academico_repository import PeriodoAcademicoRepository


router = APIRouter(prefix="/periodos-academicos",tags=["Gestión de Períodos Académicos"])
repo = PeriodoAcademicoRepository()


@router.get("/")
def listar_periodos():
    return repo.obtener_todos()


@router.get("/{periodo_id}")
def obtener_periodo(periodo_id: int):
    periodo = repo.obtener_por_id(periodo_id)

    if not periodo:
        raise HTTPException(status_code=404,detail="Período académico no encontrado")

    return periodo


@router.post("/")
def crear_periodo(periodo: PeriodoAcademico):
    nuevo_id = repo.crear(periodo)

    return {"mensaje": "Período académico registrado exitosamente","id": nuevo_id}


@router.delete("/{periodo_id}")
def eliminar_periodo(periodo_id: int):
    exito = repo.eliminar(periodo_id)

    if not exito:
        raise HTTPException(status_code=404,detail="Período académico no encontrado")

    return {"mensaje": "Período académico eliminado correctamente"}


@router.put("/{periodo_id}")
def actualizar_periodo(periodo_id: int,periodo: PeriodoAcademico):
    exito = repo.actualizar(periodo_id,periodo)

    if not exito:
        raise HTTPException(status_code=404, detail="Período académico no encontrado")

    return {"mensaje": "Período académico actualizado correctamente"}