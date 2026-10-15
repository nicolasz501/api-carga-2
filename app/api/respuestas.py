from fastapi import APIRouter, HTTPException

from app.models.Respuesta import Respuesta
from app.repositories.respuesta_repository import RespuestaRepository


router = APIRouter(prefix="/respuestas",tags=["Gestión de Respuestas"])
repo = RespuestaRepository()


@router.get("/")
def listar_respuestas():
    return repo.obtener_todos()


@router.get("/{respuesta_id}")
def obtener_respuesta(respuesta_id: int):
    respuesta = repo.obtener_por_id(respuesta_id)

    if not respuesta:
        raise HTTPException(status_code=404,detail="Respuesta no encontrada")

    return respuesta


@router.post("/")
def crear_respuesta(respuesta: Respuesta):
    nuevo_id = repo.crear(respuesta)

    return {"mensaje": "Respuesta registrada exitosamente","id": nuevo_id}


@router.delete("/{respuesta_id}")
def eliminar_respuesta(respuesta_id: int):
    exito = repo.eliminar(respuesta_id)

    if not exito:
        raise HTTPException(status_code=404,detail="Respuesta no encontrada")

    return {"mensaje": "Respuesta eliminada correctamente"}


@router.put("/{respuesta_id}")
def actualizar_respuesta(respuesta_id: int,respuesta: Respuesta):
    exito = repo.actualizar(respuesta_id,respuesta)

    if not exito:
        raise HTTPException(status_code=404,detail="Respuesta no encontrada")

    return {"mensaje": "Respuesta actualizada correctamente"}