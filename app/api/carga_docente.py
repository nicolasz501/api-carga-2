
from fastapi import APIRouter, HTTPException

from app.models.CargaDocente import CargaDocente
from app.repositories.carga_docente_repository import CargaDocenteRepository


router = APIRouter(
    prefix="/carga-docente",
    tags=["Gestión de Carga Docente"]
)

repo = CargaDocenteRepository()


@router.get("/")
def listar_carga_docente():
    try:
        return repo.obtener_todos()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar las cargas docentes"
        )


@router.get("/{carga_id}")
def obtener_carga_docente(carga_id: int):
    try:
        carga = repo.obtener_por_id(carga_id)

        if not carga:
            raise HTTPException(
                status_code=404,
                detail="Carga docente no encontrada"
            )

        return carga

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error al consultar la carga docente"
        )


@router.post("/", status_code=201)
def crear_carga_docente(carga: CargaDocente):
    try:
        nuevo_id = repo.crear(carga)

        return {
            "mensaje": "Carga docente registrada exitosamente",
            "id_carga": nuevo_id
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo registrar la carga docente. Verifica que el usuario, periodo y grupo existan."
        )


@router.put("/{carga_id}")
def actualizar_carga_docente(
    carga_id: int,
    carga: CargaDocente
):
    try:
        actualizado = repo.actualizar(carga_id, carga)

        if not actualizado:
            raise HTTPException(
                status_code=404,
                detail="Carga docente no encontrada"
            )

        return {
            "mensaje": "Carga docente actualizada correctamente"
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo actualizar la carga docente"
        )


@router.delete("/{carga_id}")
def eliminar_carga_docente(carga_id: int):
    try:
        eliminado = repo.eliminar(carga_id)

        if not eliminado:
            raise HTTPException(
                status_code=404,
                detail="Carga docente no encontrada"
            )

        return {
            "mensaje": "Carga docente eliminada correctamente"
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo eliminar la carga docente. Comprueba si existen horarios o evaluaciones asociados."
        )
