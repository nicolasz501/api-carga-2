from fastapi import APIRouter, HTTPException

from app.models.Grupo import Grupo
from app.repositories.grupo_repository import GrupoRepository


router = APIRouter(prefix="/grupos",tags=["Gestión de Grupos"])
repo = GrupoRepository()


@router.get("/")
def listar_grupos():
    return repo.obtener_todos()


@router.get("/{grupos_id}")
def obtener_grupo(grupos_id: int):
    grupo = repo.obtener_por_id(grupos_id)

    if not grupo:
        raise HTTPException(status_code=404,detail="Grupo no encontrado")

    return grupo


@router.post("/")
def crear_grupo(grupo: Grupo):
    nuevo_id = repo.crear(grupo)

    return {"mensaje": "Grupo registrado exitosamente","id": nuevo_id}


@router.delete("/{grupos_id}")
def eliminar_grupo(grupos_id: int):
    exito = repo.eliminar(grupos_id)

    if not exito:
        raise HTTPException(status_code=404,detail="Grupo no encontrado")

    return { "mensaje": "Grupo eliminado correctamente"}


@router.put("/{grupos_id}")
def actualizar_grupo(grupos_id: int,grupo: Grupo):
    exito = repo.actualizar(grupos_id,grupo)

    if not exito:
        raise HTTPException(status_code=404,detail="Grupo no encontrado")

    return {"mensaje": "Grupo actualizado correctamente"}
    