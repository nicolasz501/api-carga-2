
from fastapi import APIRouter, HTTPException, Query, Depends

from repositories import zonas as repo
from models.zonas import ZonasCrear, ZonasActualizar

from security.permisos import (
    CIUDADANO,
    FUNCIONARIO_AMBIENTAL,
    ADMINISTRADOR,
    requiere_rol,
)

router = APIRouter(
    prefix="/zonas",
    tags=["Zonas"],
)


# ==========================================
# LISTAR ZONAS
# Todos los usuarios autenticados
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
# OBTENER UNA ZONA
# Todos los usuarios autenticados
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
            detail="Zona no encontrada",
        )

    return fila


# ==========================================
# CREAR ZONA
# Solo administrador
# ==========================================
@router.post("/", status_code=201)
def crear(
    datos: ZonasCrear,
    usuario: dict = Depends(requiere_rol(ADMINISTRADOR)),
):
    try:
        return repo.crear_registro(
            datos.model_dump(exclude_unset=True)
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="No se pudo crear la zona",
        )


# ==========================================
# ACTUALIZAR ZONA
# Solo administrador
# ==========================================
@router.put("/{registro_id}")
def actualizar(
    registro_id: int,
    datos: ZonasActualizar,
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
                detail="Zona no encontrada",
            )

        return fila

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="No se pudo actualizar la zona",
        )


# ==========================================
# ELIMINAR ZONA
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
                detail="Zona no encontrada",
            )

        return {
            "mensaje": "Zona eliminada correctamente",
            "registro": fila,
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail=(
                "No se pudo eliminar la zona. "
                "Verifica si existen reportes ambientales asociados."
            ),
        )
