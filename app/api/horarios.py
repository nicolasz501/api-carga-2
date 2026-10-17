
from fastapi import APIRouter, HTTPException

from app.models.Horario import Horario
from app.repositories.horario_repository import HorarioRepository


router = APIRouter(
    prefix="/horarios",
    tags=["Gestión de Horarios"]
)

repo = HorarioRepository()


@router.get("/")
def listar_horarios():
    try:
        return repo.obtener_todos()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar los horarios"
        )


@router.get("/{horario_id}")
def obtener_horario(horario_id: int):
    try:
        horario = repo.obtener_por_id(horario_id)

        if not horario:
            raise HTTPException(
                status_code=404,
                detail="Horario no encontrado"
            )

        return horario

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar el horario"
        )


@router.post("/", status_code=201)
def crear_horario(horario: Horario):
    try:
        nuevo_id = repo.crear(horario)

        return {
            "mensaje": "Horario registrado exitosamente",
            "id_horarios": nuevo_id
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo registrar el horario. Verifica que la carga docente exista."
        )


@router.put("/{horario_id}")
def actualizar_horario(horario_id: int, horario: Horario):
    try:
        actualizado = repo.actualizar(horario_id, horario)

        if not actualizado:
            raise HTTPException(
                status_code=404,
                detail="Horario no encontrado"
            )

        return {
            "mensaje": "Horario actualizado correctamente"
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo actualizar el horario"
        )


@router.delete("/{horario_id}")
def eliminar_horario(horario_id: int):
    try:
        eliminado = repo.eliminar(horario_id)

        if not eliminado:
            raise HTTPException(
                status_code=404,
                detail="Horario no encontrado"
            )

        return {
            "mensaje": "Horario eliminado correctamente"
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo eliminar el horario"
        )
