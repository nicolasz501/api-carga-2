
from fastapi import APIRouter, HTTPException

from app.models.Pregunta import Pregunta
from app.repositories.pregunta_repository import PreguntaRepository


router = APIRouter(
    prefix="/preguntas",
    tags=["Gestión de Preguntas"]
)

repo = PreguntaRepository()


@router.get("/")
def listar_preguntas():
    try:
        return repo.obtener_todos()

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar las preguntas"
        )


@router.get("/{pregunta_id}")
def obtener_pregunta(pregunta_id: int):
    try:
        pregunta = repo.obtener_por_id(pregunta_id)

        if not pregunta:
            raise HTTPException(
                status_code=404,
                detail="Pregunta no encontrada"
            )

        return pregunta

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar la pregunta"
        )


@router.post("/", status_code=201)
def crear_pregunta(pregunta: Pregunta):
    try:
        nuevo_id = repo.crear(pregunta)

        return {
            "mensaje": "Pregunta registrada exitosamente",
            "id_preguntas": nuevo_id
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo registrar la pregunta"
        )


@router.put("/{pregunta_id}")
def actualizar_pregunta(pregunta_id: int, pregunta: Pregunta):
    try:
        actualizado = repo.actualizar(pregunta_id, pregunta)

        if not actualizado:
            raise HTTPException(
                status_code=404,
                detail="Pregunta no encontrada"
            )

        return {
            "mensaje": "Pregunta actualizada correctamente",
            "id_preguntas": pregunta_id
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo actualizar la pregunta"
        )


@router.delete("/{pregunta_id}")
def eliminar_pregunta(pregunta_id: int):
    try:
        eliminado = repo.eliminar(pregunta_id)

        if not eliminado:
            raise HTTPException(
                status_code=404,
                detail="Pregunta no encontrada"
            )

        return {
            "mensaje": "Pregunta eliminada correctamente",
            "id_preguntas": pregunta_id
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail=(
                "No se pudo eliminar la pregunta. "
                "Verifica si existen respuestas asociadas."
            )
        )
