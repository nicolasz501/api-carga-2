
from fastapi import APIRouter, HTTPException, Query, Depends

from repositories import categorias_incidente as repo
from models.categorias_incidente import (
    CategoriasIncidenteCrear,
    CategoriasIncidenteActualizar,
)
from security.permisos import (
    CIUDADANO,
    FUNCIONARIO_AMBIENTAL,
    ADMINISTRADOR,
    requiere_rol,
)

router = APIRouter(
    prefix="/categorias-incidente",
    tags=["Categorías de incidentes"],
)


# ==========================================
# LISTAR CATEGORÍAS
# Ciudadano, funcionario y administrador
# ==========================================
@router.get("/")
def listar(
    limite: int = Query(100, ge=1, le=500),
    desplazamiento: int = Query(0, ge=0),
    usuario: dict = Depends(
        requiere_rol(
            CIUDADANO,
            FUNCIONARIO_AMBIENTAL,
            ADMINISTRADOR,
        )
    ),
):
    return repo.listar_registros(limite, desplazamiento)


# ==========================================
# OBTENER UNA CATEGORÍA
# Ciudadano, funcionario y administrador
# ==========================================
@router.get("/{registro_id}")
def obtener(
    registro_id: int,
    usuario: dict = Depends(
        requiere_rol(
            CIUDADANO,
            FUNCIONARIO_AMBIENTAL,
            ADMINISTRADOR,
        )
    ),
):
    fila = repo.obtener_registro(registro_id)

    if fila is None:
        raise HTTPException(
            status_code=404,
            detail="Categoría no encontrada",
        )

    return fila


# ==========================================
# CREAR CATEGORÍA
# Solo administrador
# ==========================================
@router.post("/", status_code=201)
def crear(
    datos: CategoriasIncidenteCrear,
    usuario: dict = Depends(requiere_rol(ADMINISTRADOR)),
):
    try:
        fila = repo.crear_registro(
            datos.model_dump(exclude_unset=True)
        )
        return fila

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="No se pudo crear la categoría",
        )


# ==========================================
# ACTUALIZAR CATEGORÍA
# Solo administrador
# ==========================================
@router.put("/{registro_id}")
def actualizar(
    registro_id: int,
    datos: CategoriasIncidenteActualizar,
    usuario: dict = Depends(requiere_rol(ADMINISTRADOR)),
):
    try:
        fila = repo.actualizar_registro(
            registro_id,
            datos.model_dump(exclude_unset=True),
        )

        if fila is None:
            raise HTTPException(
                status_code=404,
                detail="Categoría no encontrada",
            )

        return fila

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


# ==========================================
# ELIMINAR CATEGORÍA
# Solo administrador
# ==========================================
@router.delete("/{registro_id}")
def eliminar(
    registro_id: int,
    usuario: dict = Depends(requiere_rol(ADMINISTRADOR)),
):
    try:
        fila = repo.eliminar_registro(registro_id)

        if fila is None:
            raise HTTPException(
                status_code=404,
                detail="Categoría no encontrada",
            )

        return {
            "mensaje": "Categoría eliminada correctamente",
            "registro": fila,
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail=(
                "No se pudo eliminar la categoría. "
                "Es posible que esté asociada a reportes existentes."
            ),
        )
