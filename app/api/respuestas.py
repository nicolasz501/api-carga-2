
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, model_validator

from app.models.Respuesta import Respuesta
from app.repositories.respuesta_repository import RespuestaRepository


router = APIRouter(
    prefix="/respuestas",
    tags=["Gestión de Respuestas"]
)

repo = RespuestaRepository()


class RespuestasLote(BaseModel):
    usuario_id: int = Field(gt=0)
    respuestas: list[Respuesta] = Field(
        min_length=5,
        max_length=5
    )
    comentario: Optional[str] = Field(
        default=None,
        max_length=2000
    )

    @model_validator(mode="after")
    def validar_preguntas_unicas(self):
        ids = [r.pregunta_id for r in self.respuestas]

        if len(set(ids)) != 5:
            raise ValueError(
                "Las cinco respuestas deben corresponder "
                "a preguntas diferentes."
            )

        return self


@router.get("/")
def listar_respuestas():
    return repo.obtener_todos()


@router.get("/{respuesta_id}")
def obtener_respuesta(respuesta_id: int):
    respuesta = repo.obtener_por_id(respuesta_id)

    if respuesta is None:
        raise HTTPException(
            status_code=404,
            detail="Respuesta no encontrada"
        )

    return respuesta


@router.post("/")
def crear_respuesta(respuesta: Respuesta):
    nuevo_id = repo.crear(respuesta)

    if nuevo_id is None:
        raise HTTPException(
            status_code=500,
            detail="No se pudo registrar la respuesta."
        )

    return {
        "mensaje": "Respuesta registrada exitosamente",
        "id": nuevo_id
    }


@router.post("/lote")
def crear_respuestas_lote(datos: RespuestasLote):
    try:
        ids = repo.crear_lote(
            respuestas=datos.respuestas,
            usuario_id=datos.usuario_id,
            comentario=datos.comentario
        )

        return {
            "mensaje": "Las cinco respuestas se registraron exitosamente.",
            "usuario_id": datos.usuario_id,
            "ids": ids,
            "total": len(ids),
            "comentario_guardado": bool(
                datos.comentario and datos.comentario.strip()
            )
        }

    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )

    except Exception as e:
        print(f"Error en POST /respuestas/lote: {e}")

        raise HTTPException(
            status_code=500,
            detail="No se pudieron registrar las respuestas."
        )


@router.delete("/{respuesta_id}")
def eliminar_respuesta(respuesta_id: int):
    exito = repo.eliminar(respuesta_id)

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Respuesta no encontrada o no se pudo eliminar."
        )

    return {
        "mensaje": "Respuesta eliminada correctamente"
    }


@router.put("/{respuesta_id}")
def actualizar_respuesta(
    respuesta_id: int,
    respuesta: Respuesta
):
    exito = repo.actualizar(respuesta_id, respuesta)

    if not exito:
        raise HTTPException(
            status_code=404,
            detail="Respuesta no encontrada o no se pudo actualizar."
        )

    return {
        "mensaje": "Respuesta actualizada correctamente"
    }
