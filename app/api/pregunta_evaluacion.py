
from fastapi import APIRouter, HTTPException, status

from app.models.PreguntaEvaluacion import PreguntaEvaluacion
from app.repositories.pregunta_evaluacion_repository import (
    PreguntaEvaluacionRepository
)


router = APIRouter(
    prefix="/preguntas-evaluaciones",
    tags=["Preguntas de Evaluaciones"]
)

repo = PreguntaEvaluacionRepository()


@router.get("/")
def listar_preguntas_evaluaciones():
    return repo.obtener_todos()


@router.get("/evaluacion/{id_evaluacion}")
def listar_por_evaluacion(id_evaluacion: int):
    try:
        return repo.obtener_por_evaluacion(id_evaluacion)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id_pregunta_evaluacion}")
def obtener_pregunta_evaluacion(id_pregunta_evaluacion: int):
    try:
        resultado = repo.obtener_por_id(id_pregunta_evaluacion)

        if not resultado:
            raise HTTPException(
                status_code=404,
                detail="La asociación pregunta-evaluación no existe."
            )

        return resultado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_pregunta_evaluacion(datos: PreguntaEvaluacion):
    try:
        return repo.crear(datos)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{id_pregunta_evaluacion}")
def actualizar_pregunta_evaluacion(
    id_pregunta_evaluacion: int,
    datos: PreguntaEvaluacion
):
    try:
        resultado = repo.actualizar(id_pregunta_evaluacion, datos)

        if not resultado:
            raise HTTPException(
                status_code=404,
                detail="La asociación pregunta-evaluación no existe."
            )

        return resultado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id_pregunta_evaluacion}")
def eliminar_pregunta_evaluacion(id_pregunta_evaluacion: int):
    try:
        resultado = repo.eliminar(id_pregunta_evaluacion)

        if not resultado:
            raise HTTPException(
                status_code=404,
                detail="La asociación pregunta-evaluación no existe."
            )

        return {
            "mensaje": "Asociación eliminada correctamente.",
            "id_pregunta_evaluacion": id_pregunta_evaluacion
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
