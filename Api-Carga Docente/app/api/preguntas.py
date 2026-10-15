from fastapi import APIRouter, HTTPException

from app.models.Pregunta import Pregunta
from app.repositories.pregunta_repository import PreguntaRepository


router = APIRouter(prefix="/preguntas",tags=["Gestión de Preguntas"])
repo = PreguntaRepository()


@router.get("/")
def listar_preguntas():
    return repo.obtener_todos()


@router.get("/{pregunta_id}")
def obtener_pregunta(pregunta_id: int):
    pregunta = repo.obtener_por_id(pregunta_id)

    if not pregunta:
        raise HTTPException(status_code=404,detail="Pregunta no encontrada")

    return pregunta


@router.post("/")
def crear_pregunta(pregunta: Pregunta):
    nuevo_id = repo.crear(pregunta)

    return {"mensaje": "Pregunta registrada exitosamente", "id": nuevo_id}


@router.delete("/{pregunta_id}")
def eliminar_pregunta(pregunta_id: int):
    exito = repo.eliminar(pregunta_id)

    if not exito:
        raise HTTPException(status_code=404,detail="Pregunta no encontrada")

    return {"mensaje": "Pregunta eliminada correctamente"}


@router.put("/{pregunta_id}")
def actualizar_pregunta(pregunta_id: int,pregunta: Pregunta):
    exito = repo.actualizar(pregunta_id, pregunta)

    if not exito:
        raise HTTPException(status_code=404,detail="Pregunta no encontrada")

    return {"mensaje": "Pregunta actualizada correctamente"}
    