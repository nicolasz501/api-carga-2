from fastapi import APIRouter, HTTPException

from app.models.Facultad import Facultad
from app.repositories.facultad_repository import FacultadRepository


router = APIRouter(prefix="/facultades",tags=["Gestión de Facultades"])
repo = FacultadRepository()


@router.get("/")
def listar_facultades():
    return repo.obtener_todos()


@router.get("/{facultades_id}")
def obtener_facultad(facultades_id: int):
    facultad = repo.obtener_por_id(facultades_id)

    if not facultad:
        raise HTTPException(status_code=404,detail="Facultad no encontrada")

    return facultad


@router.post("/")
def crear_facultad(facultad: Facultad):
    nuevo_id = repo.crear(facultad)

    return {"mensaje": "Facultad registrada exitosamente","id": nuevo_id}


@router.delete("/{facultades_id}")
def eliminar_facultad(facultades_id: int):
    exito = repo.eliminar(facultades_id)

    if not exito:
        raise HTTPException(status_code=404,detail="Facultad no encontrada")

    return {"mensaje": "Facultad eliminada correctamente"}


@router.put("/{facultades_id}")
def actualizar_facultad(facultades_id: int,facultad: Facultad):
    exito = repo.actualizar(facultades_id,facultad)

    if not exito:
        raise HTTPException(status_code=404,detail="Facultad no encontrada")

    return {"mensaje": "Facultad actualizada correctamente"}