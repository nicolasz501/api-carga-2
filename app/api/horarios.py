from fastapi import APIRouter, HTTPException

from app.models.Horario import Horario
from app.repositories.horario_repository import HorarioRepository


router = APIRouter(prefix="/horarios",tags=["Gestión de Horarios"])
repo = HorarioRepository()


@router.get("/")
def listar_horarios():
    return repo.obtener_todos()


@router.get("/{horario_id}")
def obtener_horario(horario_id: int):
    horario = repo.obtener_por_id(horario_id)

    if not horario:
        raise HTTPException(status_code=404,detail="Horario no encontrado")

    return horario


@router.post("/")
def crear_horario(horario: Horario):
    nuevo_id = repo.crear(horario)

    return {"mensaje": "Horario registrado exitosamente","id": nuevo_id}


@router.delete("/{horario_id}")
def eliminar_horario(horario_id: int):
    exito = repo.eliminar(horario_id)

    if not exito:
        raise HTTPException(status_code=404,detail="Horario no encontrado")

    return {"mensaje": "Horario eliminado correctamente"}


@router.put("/{horario_id}")
def actualizar_horario(horario_id: int,horario: Horario):
    exito = repo.actualizar(horario_id,horario)

    if not exito:
        raise HTTPException(status_code=404,detail="Horario no encontrado")

    return {"mensaje": "Horario actualizado correctamente"}
    