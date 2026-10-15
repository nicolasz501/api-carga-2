from fastapi import APIRouter, HTTPException

from app.models.Evaluacion import Evaluacion
from app.repositories.evaluacion_repository import EvaluacionRepository


router = APIRouter(prefix="/evaluaciones",tags=["Gestión de Evaluaciones"])
repo = EvaluacionRepository()


@router.get("/")
def listar_evaluaciones():
    return repo.obtener_todos()


@router.get("/{evaluacion_id}")
def obtener_evaluacion(evaluacion_id: int):
    evaluacion = repo.obtener_por_id(evaluacion_id)

    if not evaluacion:
        raise HTTPException(status_code=404,detail="Evaluación no encontrada")

    return evaluacion


@router.post("/")
def crear_evaluacion(evaluacion: Evaluacion):
    nuevo_id = repo.crear(evaluacion)

    return {"mensaje": "Evaluación registrada exitosamente","id": nuevo_id}


@router.delete("/{evaluacion_id}")
def eliminar_evaluacion(evaluacion_id: int):
    exito = repo.eliminar(evaluacion_id)

    if not exito:
        raise HTTPException(status_code=404,detail="Evaluación no encontrada")

    return {"mensaje": "Evaluación eliminada correctamente"}


@router.put("/{evaluacion_id}")
def actualizar_evaluacion(evaluacion_id: int,evaluacion: Evaluacion):
    exito = repo.actualizar(evaluacion_id,evaluacion)

    if not exito:
        raise HTTPException(status_code=404,detail="Evaluación no encontrada")

    return {"mensaje": "Evaluación actualizada correctamente"}
    