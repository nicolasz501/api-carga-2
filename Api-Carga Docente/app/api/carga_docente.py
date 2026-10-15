from fastapi import APIRouter, HTTPException

from app.models.CargaDocente import CargaDocente
from app.repositories.carga_docente_repository import CargaDocenteRepository


router = APIRouter(prefix="/carga-docente",tags=["Gestión de Carga Docente"])
repo = CargaDocenteRepository()


@router.get("/")
def listar_carga_docente():
    return repo.obtener_todos()


@router.get("/{carga_id}")
def obtener_carga_docente(carga_id: int):
    carga = repo.obtener_por_id(carga_id)

    if not carga:
        raise HTTPException(status_code=404,detail="Carga docente no encontrada")

    return carga


@router.post("/")
def crear_carga_docente(carga: CargaDocente):
    nuevo_id = repo.crear(carga)

    return {"mensaje": "Carga docente registrada exitosamente","id": nuevo_id}


@router.delete("/{carga_id}")
def eliminar_carga_docente(carga_id: int):
    exito = repo.eliminar(carga_id)

    if not exito:
        raise HTTPException(status_code=404,detail="Carga docente no encontrada")

    return {"mensaje": "Carga docente eliminada correctamente"}


@router.put("/{carga_id}")
def actualizar_carga_docente(carga_id: int,carga: CargaDocente):
    exito = repo.actualizar(carga_id,carga)

    if not exito:
        raise HTTPException(status_code=404,detail="Carga docente no encontrada")

    return {"mensaje": "Carga docente actualizada correctamente"}
    