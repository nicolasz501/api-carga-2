from fastapi import APIRouter, HTTPException
from app.models.Asignatura import Asignatura
from app.repositories.asignatura_repository import AsignaturaRepository


router = APIRouter(prefix="/asignaturas",tags=["Gestión de Asignaturas"])
repo = AsignaturaRepository()


@router.get("/")
def listar_asignaturas():
    return repo.obtener_todos()


@router.get("/{asignatura_id}")
def obtener_asignatura(asignatura_id: int):
    asignatura = repo.obtener_por_id(asignatura_id)

    if not asignatura:
        raise HTTPException(status_code=404,detail="Asignatura no encontrada")

    return asignatura


@router.post("/")
def crear_asignatura(asignatura: Asignatura):
    nuevo_id = repo.crear(asignatura)

    return {"mensaje": "Asignatura registrada exitosamente","id": nuevo_id}


@router.delete("/{asignatura_id}")
def eliminar_asignatura(asignatura_id: int):
    exito = repo.eliminar(asignatura_id)

    if not exito:
        raise HTTPException(status_code=404,detail="Asignatura no encontrada")

    return {"mensaje": "Asignatura eliminada correctamente"}


@router.put("/{asignatura_id}")
def actualizar_asignatura(asignatura_id: int,asignatura: Asignatura):
    exito = repo.actualizar(asignatura_id,asignatura)

    if not exito:
        raise HTTPException(status_code=404,detail="Asignatura no encontrada")

    return {"mensaje": "Asignatura actualizada correctamente"}