
from fastapi import APIRouter, HTTPException

from app.models.Evaluacion import Evaluacion
from app.repositories.evaluacion_repository import EvaluacionRepository


router = APIRouter(
    prefix="/evaluaciones",
    tags=["Gestión de Evaluaciones"]
)

repo = EvaluacionRepository()


@router.get("/")
def listar_evaluaciones():
    try:
        return repo.obtener_todos()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar las evaluaciones"
        )


@router.get("/{evaluacion_id}")
def obtener_evaluacion(evaluacion_id: int):
    try:
        evaluacion = repo.obtener_por_id(evaluacion_id)

        if not evaluacion:
            raise HTTPException(
                status_code=404,
                detail="Evaluación no encontrada"
            )

        return evaluacion

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar la evaluación"
        )


@router.post("/", status_code=201)
def crear_evaluacion(evaluacion: Evaluacion):
    try:
        nuevo_id = repo.crear(evaluacion)

        return {
            "mensaje": "Evaluación registrada exitosamente",
            "id_evaluaciones": nuevo_id
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo registrar la evaluación. Verifica que la carga docente exista."
        )


@router.put("/{evaluacion_id}")
def actualizar_evaluacion(
    evaluacion_id: int,
    evaluacion: Evaluacion
):
    try:
        actualizado = repo.actualizar(
            evaluacion_id,
            evaluacion
        )

        if not actualizado:
            raise HTTPException(
                status_code=404,
                detail="Evaluación no encontrada"
            )

        return {
            "mensaje": "Evaluación actualizada correctamente"
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo actualizar la evaluación"
        )


@router.delete("/{evaluacion_id}")
def eliminar_evaluacion(evaluacion_id: int):
    try:
        eliminado = repo.eliminar(evaluacion_id)

        if not eliminado:
            raise HTTPException(
                status_code=404,
                detail="Evaluación no encontrada"
            )

        return {
            "mensaje": "Evaluación eliminada correctamente"
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo eliminar la evaluación. Comprueba si tiene preguntas asociadas."
        )
