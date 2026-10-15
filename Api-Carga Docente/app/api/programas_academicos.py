from fastapi import APIRouter, HTTPException

from app.models.ProgramaAcademico import ProgramaAcademico
from app.repositories.programa_academico_repository import ProgramaAcademicoRepository


router = APIRouter(prefix="/programas-academicos",tags=["Gestión de Programas Académicos"])

repo = ProgramaAcademicoRepository()


@router.get("/")
def listar_programas():
    return repo.obtener_todos()


@router.get("/{programa_id}")
def obtener_programa(programa_id: int):
    programa = repo.obtener_por_id(programa_id)

    if not programa:
        raise HTTPException(status_code=404,detail="Programa académico no encontrado")

    return programa


@router.post("/")
def crear_programa(programa: ProgramaAcademico):
    nuevo_id = repo.crear(programa)

    return {"mensaje": "Programa académico registrado exitosamente","id": nuevo_id}


@router.delete("/{programa_id}")
def eliminar_programa(programa_id: int):
    exito = repo.eliminar(programa_id)

    if not exito:
        raise HTTPException(status_code=404,detail="Programa académico no encontrado")

    return {"mensaje": "Programa académico eliminado correctamente"}


@router.put("/{programa_id}")
def actualizar_programa(programa_id: int,programa: ProgramaAcademico):
    exito = repo.actualizar(programa_id,programa)

    if not exito:
        raise HTTPException(status_code=404,detail="Programa académico no encontrado")

    return {"mensaje": "Programa académico actualizado correctamente"}
    