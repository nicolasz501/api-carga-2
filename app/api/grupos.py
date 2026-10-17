
from fastapi import APIRouter, HTTPException

from app.models.Grupo import Grupo
from app.repositories.grupo_repository import GrupoRepository


router = APIRouter(
    prefix="/grupos",
    tags=["Gestión de Grupos"]
)

repo = GrupoRepository()


@router.get("/")
def listar_grupos():
    try:
        return repo.obtener_todos()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar los grupos"
        )


@router.get("/{grupos_id}")
def obtener_grupo(grupos_id: int):
    try:
        grupo = repo.obtener_por_id(grupos_id)

        if not grupo:
            raise HTTPException(
                status_code=404,
                detail="Grupo no encontrado"
            )

        return grupo

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar el grupo"
        )


@router.post("/", status_code=201)
def crear_grupo(grupo: Grupo):
    try:
        nuevo_id = repo.crear(grupo)

        return {
            "mensaje": "Grupo registrado exitosamente",
            "id_grupo": nuevo_id
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo registrar el grupo. Verifica que la asignatura exista."
        )


@router.put("/{grupos_id}")
def actualizar_grupo(grupos_id: int, grupo: Grupo):
    try:
        actualizado = repo.actualizar(grupos_id, grupo)

        if not actualizado:
            raise HTTPException(
                status_code=404,
                detail="Grupo no encontrado"
            )

        return {
            "mensaje": "Grupo actualizado correctamente"
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo actualizar el grupo"
        )


@router.delete("/{grupos_id}")
def eliminar_grupo(grupos_id: int):
    try:
        eliminado = repo.eliminar(grupos_id)

        if not eliminado:
            raise HTTPException(
                status_code=404,
                detail="Grupo no encontrado"
            )

        return {
            "mensaje": "Grupo eliminado correctamente"
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo eliminar el grupo. Verifica si tiene cargas docentes asociadas."
        )
